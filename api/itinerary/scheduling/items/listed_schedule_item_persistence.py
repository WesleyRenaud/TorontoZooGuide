from __future__ import annotations

from typing import Any

from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.saved_itinerary import SavedItinerary
from ..extend_departure_for_activity import cover_visit_times_for_scheduled_activity
from .listed_schedule_target import apply_listed_schedule
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_item_key import ListedScheduleItemKey
from .schedule_itinerary_helpers import build_save_result
from .schedule_itinerary_helpers import build_success_result
from .schedule_itinerary_helpers import persist_itinerary_walk_route
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ....types import ScheduleTimeKey
from ...warnings.schedule_item_not_on_itinerary_warning import schedule_item_not_on_itinerary_warning_is_required


def prepare_schedule_item_on_itinerary(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      schedule_item_key: ListedScheduleItemKey,
      *,
      itinerary_context: dict[ str, Any ],
      confirming_schedule_item_not_on_itinerary: bool,
      ) -> tuple[ list[ ItineraryErrorType ], ItinerarySaveResult | None ]:
   suppressed_warnings: list[ ItineraryErrorType ] = []

   if schedule_item_not_on_itinerary_warning_is_required(
         conn,
         saved_itinerary,
         schedule_item_key,
         confirming_schedule_item_not_on_itinerary=(
            confirming_schedule_item_not_on_itinerary
         ),
         suppressed_warnings=suppressed_warnings ):
      return (
         suppressed_warnings,
         build_save_result(
            conn,
            ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
            suppressed_warnings=suppressed_warnings,
            **itinerary_context ),
      )

   return ( suppressed_warnings, None )


def commit_listed_schedule(
      conn: Connection,
      *,
      schedule_item_key: ListedScheduleItemKey,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      insert_if_missing: bool,
      itinerary_context: dict[ str, Any ] ) -> ItinerarySaveResult:
   cur = conn.cursor()

   try:
      scheduled = apply_listed_schedule(
         cur,
         schedule_item_key,
         start_time,
         end_time,
         insert_if_missing )

      if not scheduled:
         return build_save_result(
            conn,
            ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
            **itinerary_context )

      conn.commit()

   finally:
      cur.close()

   saved_itinerary = fetch_saved_itinerary( conn )
   cover_visit_times_for_scheduled_activity(
      conn,
      start_time=start_time,
      end_time=end_time,
      current_arrival_time=saved_itinerary.arrival_time,
      current_departure_time=saved_itinerary.departure_time,
      itinerary_context=itinerary_context )

   persist_itinerary_walk_route( conn, **itinerary_context )

   return build_success_result( conn, **itinerary_context )
