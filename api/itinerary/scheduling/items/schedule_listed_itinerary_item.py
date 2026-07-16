from __future__ import annotations

from typing import Any

from ...data_access.find_saved_itinerary_schedule_item_row import saved_schedule_item_is_already_scheduled
from ...data_access.itinerary import fetch_saved_itinerary
from .listed_schedule_item_persistence import commit_listed_schedule
from .listed_schedule_item_persistence import prepare_schedule_item_on_itinerary
from .listed_schedule_target import resolve_listed_schedule_target
from .parse_schedule_time_options import ParsedScheduleTimeOptions
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_item_key import ListedScheduleItemKey
from .schedule_itinerary_helpers import build_save_result
from .schedule_itinerary_helpers import effective_duration_seconds
from .schedule_itinerary_helpers import prepare_schedule_window
from .schedule_itinerary_helpers import resolve_slot_times_allowing_visit_extension
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ...warnings.itinerary_suppressed_warnings import with_suppressed_warnings
from ...warnings.schedule_item_not_on_itinerary_warning import saved_itinerary_has_schedule_item


def schedule_listed_itinerary_item(
      conn: Connection,
      schedule_item_key: ListedScheduleItemKey,
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

   target = resolve_listed_schedule_target( conn, schedule_item_key )

   duration_seconds = effective_duration_seconds(
      time_options.duration_minutes,
      target.default_duration_seconds )

   if duration_seconds is None:
      return build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_context )

   slot, slot_error = resolve_slot_times_allowing_visit_extension(
      conn,
      saved_itinerary,
      prepared_window.window,
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
