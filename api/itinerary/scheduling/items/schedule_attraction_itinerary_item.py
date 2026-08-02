from __future__ import annotations

from typing import Any

from ...attraction_item_key import AttractionScheduleItemKey
from ....attractions.scheduling.attraction_operating_hours import fetch_configured_attraction_operating_hours_seconds
from ...data_access.find_saved_itinerary_schedule_item_row import saved_schedule_item_is_already_scheduled
from ...data_access.itinerary import fetch_itinerary_date
from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.itinerary_default_duration import fetch_attraction_default_duration_seconds
from .listed_schedule_item_persistence import commit_listed_schedule
from .listed_schedule_item_persistence import prepare_schedule_item_on_itinerary
from .parse_schedule_time_options import ParsedScheduleTimeOptions
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_itinerary_helpers import build_save_result
from .schedule_itinerary_helpers import effective_duration_seconds
from .schedule_itinerary_helpers import prepare_schedule_window
from .schedule_itinerary_helpers import resolve_slot_times
from .schedule_itinerary_helpers import resolve_slot_times_allowing_visit_extension
from ....shared.calendar_dates import DateValues
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ...warnings.itinerary_suppressed_warnings import with_suppressed_warnings
from ...warnings.schedule_item_not_on_itinerary_warning import saved_itinerary_has_schedule_item
from ....zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record


def schedule_attraction_itinerary_item(
      conn: Connection,
      schedule_item_key: AttractionScheduleItemKey,
      time_options: ParsedScheduleTimeOptions,
      *,
      itinerary_context: dict[ str, Any ],
      confirming_schedule_item_not_on_itinerary: bool,
      ) -> ItinerarySaveResult:
   saved_itinerary = fetch_saved_itinerary( conn )
   prepared_window = prepare_schedule_window(
      conn,
      saved_itinerary,
      **itinerary_context )

   if isinstance( prepared_window, ItinerarySaveResult ):
      return prepared_window

   schedule_window = prepared_window.window
   attraction_hours = _configured_attraction_hours_for_itinerary(
      conn,
      schedule_item_key.name )

   if attraction_hours is not None:
      schedule_window = (
         max( schedule_window[ 0 ], attraction_hours[ 0 ] ),
         min( schedule_window[ 1 ], attraction_hours[ 1 ] ) )

      if schedule_window[ 0 ] >= schedule_window[ 1 ]:
         return build_save_result(
            conn,
            ItineraryErrorType.NO_AVAILABLE_SLOT,
            **itinerary_context )

   suppressed_warnings, membership_error = prepare_schedule_item_on_itinerary(
      conn,
      saved_itinerary,
      schedule_item_key,
      itinerary_context=itinerary_context,
      confirming_schedule_item_not_on_itinerary=(
         confirming_schedule_item_not_on_itinerary
      ) )

   if membership_error is not None:
      return membership_error

   if saved_schedule_item_is_already_scheduled(
         saved_itinerary,
         schedule_item_key ):
      return with_suppressed_warnings(
         build_save_result(
            conn,
            ItineraryErrorType.ITEM_ALREADY_SCHEDULED,
            **itinerary_context ),
         suppressed_warnings )

   duration_seconds = effective_duration_seconds(
      time_options.duration_minutes,
      fetch_attraction_default_duration_seconds(
         conn,
         schedule_item_key.name ) )

   if duration_seconds is None:
      return build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_context )

   if attraction_hours is None:
      slot, slot_error = resolve_slot_times_allowing_visit_extension(
         conn,
         saved_itinerary,
         schedule_window,
         duration_seconds,
         start_time=time_options.start_time,
         itinerary_context=itinerary_context )
   else:
      slot, slot_error = resolve_slot_times(
         conn,
         saved_itinerary,
         schedule_window,
         duration_seconds,
         start_time=time_options.start_time,
         itinerary_context=itinerary_context )

   if slot_error is not None:
      return slot_error

   start_time_key, end_time = slot

   return with_suppressed_warnings(
      commit_listed_schedule(
         conn,
         schedule_item_key=schedule_item_key,
         start_time=start_time_key,
         end_time=end_time,
         insert_if_missing=not saved_itinerary_has_schedule_item(
            saved_itinerary,
            schedule_item_key ),
         itinerary_context=itinerary_context ),
      suppressed_warnings )


def _configured_attraction_hours_for_itinerary(
      conn: Connection,
      attraction_name: str,
) -> tuple[ int, int ] | None:
   visit_date = fetch_itinerary_date( conn )
   parsed_visit_date = DateValues.parse_date_value( visit_date )

   if parsed_visit_date is None:
      return None

   zoo_hours_record = fetch_zoo_hours_record( conn, visit_date )

   if zoo_hours_record is None:
      return None

   zoo_open_seconds = DateValues.time_value_in_seconds(
      zoo_hours_record.open_time )
   zoo_close_seconds = DateValues.time_value_in_seconds(
      zoo_hours_record.close_time )

   if zoo_open_seconds is None or zoo_close_seconds is None:
      return None

   return fetch_configured_attraction_operating_hours_seconds(
      conn,
      attraction_name,
      visit_date=parsed_visit_date,
      zoo_open_seconds=zoo_open_seconds,
      zoo_close_seconds=zoo_close_seconds )
