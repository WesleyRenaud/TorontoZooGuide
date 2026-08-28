from __future__ import annotations

from typing import Any

from ...animal_schedule_item_key import AnimalScheduleItemKey
from ...attraction_schedule_item_key import AttractionScheduleItemKey
from ...data_access.attraction_also_transportation_provider import AttractionAlsoTransportationProvider
from ...data_access.itinerary_provider import ItineraryProvider
from ...data_access.saved_itinerary_schedule_item_row_finder import SavedItineraryScheduleItemRowFinder
from .itinerary_save_result_builder import ItinerarySaveResultBuilder
from .listed_schedule_item_key import ListedScheduleItemKey
from .listed_schedule_item_persister import ListedScheduleItemPersister
from .listed_schedule_target_resolver import ListedScheduleTargetResolver
from .parsed_schedule_time_options import ParsedScheduleTimeOptions
from ...results.itinerary_save_result import ItinerarySaveResult
from ...routing.transportation_walk_node_resolver import TransportationWalkNodeResolver
from .schedule_item_travel_time_calculator import ScheduleItemTravelTimeCalculator
from .schedule_slot_time_resolver import ScheduleSlotTimeResolver
from .schedule_window_preparer import ScheduleWindowPreparer
from ....shared.enums import ItineraryErrorType
from ....types import Types
from ...warnings.itinerary_suppressed_warnings_builder import ItinerarySuppressedWarningsBuilder
from ...warnings.schedule_item_not_on_itinerary_warning_builder import ScheduleItemNotOnItineraryWarningBuilder


class ListedItineraryItemScheduler():
   @classmethod
   def schedule(
         cls,
         conn: Types.Connection,
         schedule_item_key: ListedScheduleItemKey.Key,
         time_options: ParsedScheduleTimeOptions,
         *,
         itinerary_context: dict[ str, Any ],
         confirming_schedule_item_not_on_itinerary: bool,
         ) -> ItinerarySaveResult:
      saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )
      prepared_window = ScheduleWindowPreparer.prepare(
         conn,
         saved_itinerary,
         **itinerary_context )

      if isinstance( prepared_window, ItinerarySaveResult ):
         return prepared_window

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

      target = ListedScheduleTargetResolver.resolve( conn, schedule_item_key )

      duration_seconds = ScheduleSlotTimeResolver.effective_duration_seconds(
         time_options.duration_minutes,
         target.default_duration_seconds )

      if duration_seconds is None:
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.SAVE_FAILED,
            **itinerary_context )

      candidate_walk_node_id = cls._walk_node_id_for_listed_item(
         conn,
         schedule_item_key )
      visit_anchor_seconds = prepared_window.window[ 0 ]
      earliest_start_seconds = ScheduleItemTravelTimeCalculator.earliest_schedule_start_seconds_with_travel(
         saved_itinerary,
         candidate_walk_node_id=candidate_walk_node_id,
         visit_anchor_seconds=visit_anchor_seconds,
         itinerary_context=itinerary_context,
         start_time=time_options.start_time )

      slot, slot_error = ScheduleSlotTimeResolver.resolve_allowing_visit_extension(
         conn,
         saved_itinerary,
         prepared_window.window,
         duration_seconds,
         start_time=time_options.start_time,
         itinerary_context=itinerary_context,
         earliest_start_seconds=earliest_start_seconds )

      if slot_error is not None:
         return slot_error

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
   def _walk_node_id_for_listed_item(
         cls,
         conn: Types.Connection,
         schedule_item_key: ListedScheduleItemKey.Key ) -> str | None:
      if isinstance( schedule_item_key, AnimalScheduleItemKey ):
         return ScheduleItemTravelTimeCalculator.walk_node_id_for_animal(
            species=schedule_item_key.species,
            exhibit=schedule_item_key.exhibit,
            enclosure_name=schedule_item_key.enclosure_name )

      if isinstance( schedule_item_key, AttractionScheduleItemKey ):
         if AttractionAlsoTransportationProvider.attraction_is_also_transportation(
               conn,
               schedule_item_key.name ):
            return TransportationWalkNodeResolver.resolve( schedule_item_key.name )

         return ScheduleItemTravelTimeCalculator.walk_node_id_for_attraction( schedule_item_key.name )

      return None
