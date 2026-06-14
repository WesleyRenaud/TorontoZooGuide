from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from typing import Any

from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.itinerary_default_duration import fetch_attraction_default_duration_seconds
from ...data_access.itinerary_default_duration import fetch_enclosure_default_duration_seconds
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.schedule_itinerary_item import insert_itinerary_animal_schedule
from ...data_access.schedule_itinerary_item import insert_itinerary_attraction_schedule
from ...data_access.schedule_itinerary_item import update_itinerary_animal_schedule
from ...data_access.schedule_itinerary_item import update_itinerary_attraction_schedule
from .parse_schedule_item_request import ParsedScheduleItemRequest
from .parse_schedule_time_options import ParsedScheduleTimeOptions
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_itinerary_helpers import build_save_result
from .schedule_itinerary_helpers import build_success_result
from .schedule_itinerary_helpers import effective_duration_seconds
from .schedule_itinerary_helpers import resolve_schedule_window
from .schedule_itinerary_helpers import resolve_slot_times
from ....shared.enums import ItineraryErrorType
from ....shared.enums import ScheduleItemKind
from ....types import Connection
from ....types import Cursor
from ....types import ScheduleTimeKey
from ...warnings.itinerary_suppressed_warnings import with_suppressed_warnings
from ...warnings.schedule_item_not_on_itinerary_warning import saved_itinerary_has_schedule_item
from ...warnings.schedule_item_not_on_itinerary_warning import schedule_item_not_on_itinerary_warning_is_required


@dataclass( frozen=True )
class ListedScheduleTarget:
   default_duration_seconds: int | None
   apply_schedule: Callable[
      [ Cursor, ScheduleTimeKey, ScheduleTimeKey, bool ],
      bool,
   ]


def _prepare_schedule_item_on_itinerary(
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


def _apply_itinerary_animal_schedule(
      cur: Cursor,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      insert_if_missing: bool,
      *,
      species: str,
      exhibit: str ) -> bool:
   if insert_if_missing:
      inserted = insert_itinerary_animal_schedule(
         cur,
         species=species,
         exhibit=exhibit,
         start_time=start_time,
         end_time=end_time )

      if inserted:
         return True

   return update_itinerary_animal_schedule(
      cur,
      species=species,
      exhibit=exhibit,
      start_time=start_time,
      end_time=end_time )


def _apply_itinerary_attraction_schedule(
      cur: Cursor,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      insert_if_missing: bool,
      *,
      name: str ) -> bool:
   if insert_if_missing:
      inserted = insert_itinerary_attraction_schedule(
         cur,
         name=name,
         start_time=start_time,
         end_time=end_time )

      if inserted:
         return True

   return update_itinerary_attraction_schedule(
      cur,
      name=name,
      start_time=start_time,
      end_time=end_time )


def _resolve_listed_schedule_target(
      conn: Connection,
      parsed: ParsedScheduleItemRequest ) -> ListedScheduleTarget:
   if parsed.kind == ScheduleItemKind.ANIMAL:
      return ListedScheduleTarget(
         default_duration_seconds=fetch_enclosure_default_duration_seconds(
            conn,
            parsed.species,
            parsed.exhibit ),
         apply_schedule=partial(
            _apply_itinerary_animal_schedule,
            species=parsed.species,
            exhibit=parsed.exhibit ) )

   return ListedScheduleTarget(
      default_duration_seconds=fetch_attraction_default_duration_seconds(
         conn,
         parsed.attraction_name ),
      apply_schedule=partial(
         _apply_itinerary_attraction_schedule,
         name=parsed.attraction_name ) )


def _commit_listed_schedule(
      conn: Connection,
      *,
      apply_schedule: Callable[
         [ Cursor, ScheduleTimeKey, ScheduleTimeKey, bool ],
         bool,
      ],
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      insert_if_missing: bool,
      itinerary_context: dict[ str, Any ] ) -> ItinerarySaveResult:
   cur = conn.cursor()

   try:
      scheduled = apply_schedule(
         cur,
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

   return build_success_result( conn, **itinerary_context )


def schedule_listed_itinerary_item(
      conn: Connection,
      parsed: ParsedScheduleItemRequest,
      time_options: ParsedScheduleTimeOptions,
      *,
      itinerary_context: dict[ str, Any ],
      confirming_schedule_item_not_on_itinerary: bool,
      ) -> ItinerarySaveResult:
   saved_itinerary = fetch_saved_itinerary( conn )
   window = resolve_schedule_window(
      conn,
      saved_itinerary,
      **itinerary_context )

   if isinstance( window, ItinerarySaveResult ):
      return window

   suppressed_warnings, membership_error = _prepare_schedule_item_on_itinerary(
      conn,
      saved_itinerary,
      parsed,
      itinerary_context=itinerary_context,
      confirming_schedule_item_not_on_itinerary=(
         confirming_schedule_item_not_on_itinerary
      ) )

   if membership_error is not None:
      return membership_error

   target = _resolve_listed_schedule_target( conn, parsed )

   duration_seconds = effective_duration_seconds(
      time_options.duration_minutes,
      target.default_duration_seconds )

   if duration_seconds is None:
      return build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_context )

   slot, slot_error = resolve_slot_times(
      conn,
      saved_itinerary,
      window,
      duration_seconds,
      start_time=time_options.start_time,
      itinerary_context=itinerary_context )

   if slot_error is not None:
      return slot_error

   start_time_key, end_time = slot

   return with_suppressed_warnings(
      _commit_listed_schedule(
         conn,
         apply_schedule=target.apply_schedule,
         start_time=start_time_key,
         end_time=end_time,
         insert_if_missing=not saved_itinerary_has_schedule_item( saved_itinerary, parsed ),
         itinerary_context=itinerary_context ),
      suppressed_warnings )
