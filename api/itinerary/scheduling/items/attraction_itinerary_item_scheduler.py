from __future__ import annotations

from typing import Any

from .attraction_or_transportation_duration_resolver import AttractionOrTransportationDurationResolver
from ...attraction_schedule_item_key import AttractionScheduleItemKey
from ....attractions.scheduling.attraction_hours_schedule_adjustment import AttractionHoursScheduleAdjustment
from ....attractions.scheduling.attraction_operating_hours_resolver import AttractionOperatingHoursResolver
from ..core.available_schedule_slot_finder import AvailableScheduleSlotFinder
from ..core.time_block_builder import TimeBlockBuilder
from ...data_access.itinerary_provider import ItineraryProvider
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.saved_itinerary_schedule_item_row_finder import SavedItineraryScheduleItemRowFinder
from ...domain.itinerary_builder import ItineraryBuilder
from .itinerary_save_result_builder import ItinerarySaveResultBuilder
from .listed_schedule_item_persister import ListedScheduleItemPersister
from .parsed_schedule_time_options import ParsedScheduleTimeOptions
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_item_travel_time_calculator import ScheduleItemTravelTimeCalculator
from .schedule_slot_time_resolver import ScheduleSlotTimeResolver
from .schedule_window_preparer import ScheduleWindowPreparer
from ....shared.calendar_dates import DateValues
from ....shared.enums import ItineraryErrorType
from ....shared.operating_hours import OperatingHours
from ....types import Types
from ...warnings.itinerary_suppressed_warnings_builder import ItinerarySuppressedWarningsBuilder
from ...warnings.schedule_item_not_on_itinerary_warning_builder import ScheduleItemNotOnItineraryWarningBuilder


class AttractionItineraryItemScheduler():
   @classmethod
   def schedule(
         cls,
         conn: Types.Connection,
         schedule_item_key: AttractionScheduleItemKey,
         time_options: ParsedScheduleTimeOptions,
         *,
         itinerary_context: dict[ str, Any ],
         confirming_schedule_item_not_on_itinerary: bool,
         confirming_attraction_outside_operating_hours: bool,
         ) -> ItinerarySaveResult:
      saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )
      prepared_window = ScheduleWindowPreparer.prepare(
         conn,
         saved_itinerary,
         **itinerary_context )

      if isinstance( prepared_window, ItinerarySaveResult ):
         return prepared_window

      schedule_window = prepared_window.window
      attraction_hours = (
         None
         if prepared_window.zoo_operating_hours is None
         else AttractionOperatingHoursResolver.fetch_configured_operating_hours_seconds(
            conn,
            schedule_item_key.name,
            visit_date=prepared_window.visit_date,
            zoo_operating_hours=prepared_window.zoo_operating_hours,
         )
      )

      if attraction_hours is not None:
         schedule_window = (
            max( schedule_window[ 0 ], attraction_hours.open_seconds ),
            min( schedule_window[ 1 ], attraction_hours.close_seconds ) )

         if schedule_window[ 0 ] >= schedule_window[ 1 ]:
            return ItinerarySaveResultBuilder.save_result(
               conn,
               ItineraryErrorType.NO_AVAILABLE_SLOT,
               **itinerary_context )

      suppressed_warnings, membership_error = ListedScheduleItemPersister.prepare(
         conn,
         saved_itinerary,
         schedule_item_key,
         itinerary_context=itinerary_context,
         confirming_schedule_item_not_on_itinerary=(
            confirming_schedule_item_not_on_itinerary
         ) )

      if membership_error is not None:
         return membership_error

      if SavedItineraryScheduleItemRowFinder.saved_schedule_item_is_already_scheduled(
            saved_itinerary,
            schedule_item_key ):
         return ItinerarySuppressedWarningsBuilder.with_suppressed_warnings(
            ItinerarySaveResultBuilder.save_result(
               conn,
               ItineraryErrorType.ITEM_ALREADY_SCHEDULED,
               **itinerary_context ),
            suppressed_warnings )

      duration_seconds = ScheduleSlotTimeResolver.effective_duration_seconds(
         time_options.duration_minutes,
         AttractionOrTransportationDurationResolver.default_seconds(
            conn,
            schedule_item_key.name ) )

      if duration_seconds is None:
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.SAVE_FAILED,
            **itinerary_context )

      hours_adjustment = cls._attraction_hours_adjustment_for_requested_time(
         time_options.start_time,
         duration_seconds=duration_seconds,
         attraction_hours=attraction_hours )

      if (
            hours_adjustment is not None
            and not confirming_attraction_outside_operating_hours ):
         return ItinerarySuppressedWarningsBuilder.with_suppressed_warnings(
            ItinerarySaveResultBuilder.save_result(
               conn,
               ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS,
               **itinerary_context ),
            suppressed_warnings )

      if hours_adjustment is not None:
         slot, slot_error = cls._resolve_adjusted_attraction_slot(
            conn,
            saved_itinerary,
            schedule_window,
            duration_seconds,
            hours_adjustment=hours_adjustment,
            itinerary_context=itinerary_context )
      else:
         earliest_start_seconds = ScheduleItemTravelTimeCalculator.earliest_schedule_start_seconds_with_travel(
            saved_itinerary,
            candidate_walk_node_id=ScheduleItemTravelTimeCalculator.walk_node_id_for_attraction(
               schedule_item_key.name ),
            visit_anchor_seconds=schedule_window[ 0 ],
            itinerary_context=itinerary_context,
            start_time=time_options.start_time )
         slot, slot_error = ScheduleSlotTimeResolver.resolve_allowing_visit_extension(
            conn,
            saved_itinerary,
            schedule_window,
            duration_seconds,
            start_time=time_options.start_time,
            itinerary_context=itinerary_context,
            day_hours_window=(
               None
               if attraction_hours is None
               else (
                  attraction_hours.open_seconds,
                  attraction_hours.close_seconds,
               )
            ),
            earliest_start_seconds=earliest_start_seconds )

      if slot_error is not None:
         return ItinerarySuppressedWarningsBuilder.with_suppressed_warnings( slot_error, suppressed_warnings )

      start_time_key, end_time = slot

      return ItinerarySuppressedWarningsBuilder.with_suppressed_warnings(
         ListedScheduleItemPersister.commit(
            conn,
            schedule_item_key=schedule_item_key,
            start_time=start_time_key,
            end_time=end_time,
            insert_if_missing=not ScheduleItemNotOnItineraryWarningBuilder.saved_itinerary_has_schedule_item(
               saved_itinerary,
               schedule_item_key ),
            itinerary_context=itinerary_context ),
         suppressed_warnings )


   @classmethod
   def _attraction_hours_adjustment_for_requested_time(
         cls,
         start_time: Types.ScheduleTimeKey,
         *,
         duration_seconds: int,
         attraction_hours: OperatingHours | None,
   ) -> AttractionHoursScheduleAdjustment | None:
      if start_time is None or attraction_hours is None:
         return None

      start_seconds = DateValues.time_value_in_seconds( start_time )

      if start_seconds is None:
         return None

      open_seconds = attraction_hours.open_seconds
      close_seconds = attraction_hours.close_seconds

      if start_seconds < open_seconds:
         return AttractionHoursScheduleAdjustment.BEFORE_OPEN

      if start_seconds + duration_seconds > close_seconds:
         return AttractionHoursScheduleAdjustment.AFTER_CLOSE

      return None


   @classmethod
   def _resolve_adjusted_attraction_slot(
         cls,
         conn: Types.Connection,
         saved_itinerary: SavedItinerary,
         schedule_window: tuple[ int, int ],
         duration_seconds: int,
         *,
         hours_adjustment: AttractionHoursScheduleAdjustment,
         itinerary_context: dict[ str, Any ],
   ) -> tuple[ tuple[ Types.ScheduleTimeKey, Types.ScheduleTimeKey ] | None, ItinerarySaveResult | None ]:
      if hours_adjustment == AttractionHoursScheduleAdjustment.BEFORE_OPEN:
         return ScheduleSlotTimeResolver.resolve(
            conn,
            saved_itinerary,
            schedule_window,
            duration_seconds,
            start_time=None,
            itinerary_context=itinerary_context )

      itinerary = ItineraryBuilder.build_current( saved_itinerary, **itinerary_context )
      blockers = TimeBlockBuilder.collect_from_itinerary( itinerary )
      anchor_seconds, day_end_seconds = schedule_window
      slot = AvailableScheduleSlotFinder.find_previous(
         blockers,
         end_before_seconds=day_end_seconds,
         duration_seconds=duration_seconds,
         day_start_seconds=anchor_seconds )

      if slot is None:
         return None, ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.NO_AVAILABLE_SLOT,
            **itinerary_context )

      return slot, None
