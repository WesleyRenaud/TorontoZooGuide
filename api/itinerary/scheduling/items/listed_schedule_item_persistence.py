from __future__ import annotations

from typing import Any

from ...data_access.saved_itinerary import SavedItinerary
from .listed_schedule_target import apply_listed_schedule
from .parse_schedule_item_request import ParsedScheduleItemRequest
from ...results.itinerary_save_result import ItinerarySaveResult
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
      parsed: ParsedScheduleItemRequest,
      *,
      itinerary_context: dict[ str, Any ],
      confirming_schedule_item_not_on_itinerary: bool,
      ) -> tuple[ tuple[ ItineraryErrorType, ... ], ItinerarySaveResult | None ]:
   suppressed_warnings: list[ ItineraryErrorType ] = []

   if schedule_item_not_on_itinerary_warning_is_required(
         conn,
         saved_itinerary,
         parsed,
         confirming_schedule_item_not_on_itinerary=(
            confirming_schedule_item_not_on_itinerary
         ),
         suppressed_warnings=suppressed_warnings ):
      warning_tuple = tuple( suppressed_warnings )
      return (
         warning_tuple,
         build_save_result(
            conn,
            ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
            suppressed_warnings=warning_tuple,
            **itinerary_context ),
      )

   return ( tuple( suppressed_warnings ), None )


def commit_listed_schedule(
      conn: Connection,
      *,
      parsed: ParsedScheduleItemRequest,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      insert_if_missing: bool,
      itinerary_context: dict[ str, Any ] ) -> ItinerarySaveResult:
   cur = conn.cursor()

   try:
      scheduled = apply_listed_schedule(
         cur,
         parsed,
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

   persist_itinerary_walk_route( conn, **itinerary_context )

   return build_success_result( conn, **itinerary_context )
