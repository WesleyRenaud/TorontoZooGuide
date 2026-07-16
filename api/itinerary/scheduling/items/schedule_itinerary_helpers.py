from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from ....animals.coordinators.animal_coordinator import AnimalCoordinator
from ....attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..core.find_next_available_slot import find_available_slot_before_or_after_bounds
from ..core.resolve_schedule_slot import resolve_schedule_slot
from ..core.scheduling_anchor import scheduling_anchor_seconds_covering_fixed_zoo_starts
from ..core.scheduling_anchor import scheduling_day_end_seconds
from ..core.time_block import collect_time_blocks_from_itinerary
from ...data_access.itinerary import fetch_itinerary_date
from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.itinerary_status import is_itinerary_error_suppressed
from ...data_access.itinerary_time import set_itinerary_arrival_time
from ...data_access.saved_itinerary import SavedItinerary
from ...domain.itinerary import build_current_itinerary
from ...domain.itinerary_adjustment import ItineraryAdjustment
from ....guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ...results.itinerary_result_reason import ItineraryResultReason
from ...results.itinerary_save_result import ItinerarySaveResult
from ....shared.duration_values import duration_minutes_to_seconds
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ....types import ScheduleTimeKey
from ...validation.fixed_zoo_schedule_start_times import fixed_zoo_schedule_start_times_from_saved_itinerary
from ...validation.itinerary_arrival_time_validation import earliest_arrival_time
from ....wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from ....zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record
from ....zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


@dataclass( frozen=True )
class PreparedScheduleWindow:
   saved_itinerary: SavedItinerary
   window: tuple[ int, int ]


def build_itinerary_context(
      *,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      visit_date_temp: float | None = None ) -> dict[ str, Any ]:
   return {
      'animal_coordinator': animal_coordinator,
      'attraction_coordinator': attraction_coordinator,
      'guardians_coordinator': guardians_coordinator,
      'wild_encounter_coordinator': wild_encounter_coordinator,
      'visit_date_temp': visit_date_temp,
   }


def build_save_result(
      conn: Connection,
      status: ItineraryErrorType,
      *,
      reasons: tuple[ ItineraryResultReason, ... ] = (),
      suppressed_warnings: tuple[ ItineraryErrorType, ... ] = (),
      **itinerary_context: Any ) -> ItinerarySaveResult:
   return ItinerarySaveResult(
      status=status,
      reasons=reasons,
      suppressed_warnings=suppressed_warnings,
      itinerary=build_current_itinerary(
         fetch_saved_itinerary( conn ),
         **itinerary_context ) )


def build_success_result(
      conn: Connection,
      *,
      adjustments: tuple[ ItineraryAdjustment, ... ] = (),
      suppressed_warnings: tuple[ ItineraryErrorType, ... ] = (),
      **itinerary_context: Any ) -> ItinerarySaveResult:
   return ItinerarySaveResult(
      adjustments=adjustments,
      suppressed_warnings=suppressed_warnings,
      itinerary=build_current_itinerary(
         fetch_saved_itinerary( conn ),
         **itinerary_context ) )


def persist_itinerary_walk_route(
      conn: Connection,
      **itinerary_context: Any ) -> None:
   from ...routing.persist_itinerary_walk_route import rebuild_and_persist_itinerary_walk_route

   rebuild_and_persist_itinerary_walk_route( conn, **itinerary_context )


def prepare_schedule_window(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      *,
      ensure_arrival_at_zoo_open: bool = False,
      **itinerary_context: Any ) -> PreparedScheduleWindow | ItinerarySaveResult:
   visit_date = fetch_itinerary_date( conn )

   if visit_date is None:
      return build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_context )

   zoo_hours_record = fetch_zoo_hours_record( conn, visit_date )
   allow_early_admission = _early_admission_scheduling_is_allowed( conn )

   if ensure_arrival_at_zoo_open:
      saved_itinerary = _ensure_arrival_at_zoo_open(
         conn,
         saved_itinerary,
         zoo_hours_record,
         allow_early_admission=allow_early_admission )

   fixed_zoo_start_times = fixed_zoo_schedule_start_times_from_saved_itinerary(
      saved_itinerary )
   anchor_seconds = scheduling_anchor_seconds_covering_fixed_zoo_starts(
      zoo_hours_record,
      saved_itinerary.arrival_time,
      fixed_zoo_start_times,
      allow_early_admission=allow_early_admission )
   day_end_seconds = scheduling_day_end_seconds(
      zoo_hours_record,
      saved_itinerary.departure_time )

   if anchor_seconds is None or day_end_seconds is None:
      return build_save_result(
         conn,
         ItineraryErrorType.SCHEDULE_WINDOW_UNAVAILABLE,
         **itinerary_context )

   return PreparedScheduleWindow(
      saved_itinerary=saved_itinerary,
      window=( anchor_seconds, day_end_seconds ) )


def prepare_zoo_hours_schedule_window(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      *,
      ensure_arrival_at_zoo_open: bool = True,
      **itinerary_context: Any ) -> PreparedScheduleWindow | ItinerarySaveResult:
   visit_date = fetch_itinerary_date( conn )

   if visit_date is None:
      return build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_context )

   zoo_hours_record = fetch_zoo_hours_record( conn, visit_date )
   allow_early_admission = _early_admission_scheduling_is_allowed( conn )

   if ensure_arrival_at_zoo_open:
      saved_itinerary = _ensure_arrival_at_zoo_open(
         conn,
         saved_itinerary,
         zoo_hours_record,
         allow_early_admission=allow_early_admission )

   window = zoo_hours_schedule_window_seconds(
      zoo_hours_record,
      fixed_zoo_start_times=(
         fixed_zoo_schedule_start_times_from_saved_itinerary( saved_itinerary ) ),
      allow_early_admission=allow_early_admission )

   if window is None:
      return build_save_result(
         conn,
         ItineraryErrorType.SCHEDULE_WINDOW_UNAVAILABLE,
         **itinerary_context )

   return PreparedScheduleWindow(
      saved_itinerary=saved_itinerary,
      window=window )


def zoo_hours_schedule_window_seconds(
      zoo_hours_record: ZooHoursRecord | None,
      *,
      fixed_zoo_start_times: Iterable[ ScheduleTimeKey ] = (),
      allow_early_admission: bool = False ) -> tuple[ int, int ] | None:
   anchor_seconds = scheduling_anchor_seconds_covering_fixed_zoo_starts(
      zoo_hours_record,
      None,
      fixed_zoo_start_times,
      allow_early_admission=allow_early_admission )
   day_end_seconds = scheduling_day_end_seconds( zoo_hours_record, None )

   if anchor_seconds is None or day_end_seconds is None:
      return None

   return ( anchor_seconds, day_end_seconds )


def _early_admission_scheduling_is_allowed( conn: Connection ) -> bool:
   return is_itinerary_error_suppressed(
      conn,
      ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP )


def _ensure_arrival_at_zoo_open(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      zoo_hours_record: ZooHoursRecord | None,
      *,
      allow_early_admission: bool = False ) -> SavedItinerary:
   if saved_itinerary.arrival_time is not None:
      return saved_itinerary

   if zoo_hours_record is None:
      return saved_itinerary

   arrival_time = (
      earliest_arrival_time( zoo_hours_record )
      if allow_early_admission
      else zoo_hours_record.open_time )

   if arrival_time is None:
      return saved_itinerary

   set_itinerary_arrival_time( conn, arrival_time )
   return fetch_saved_itinerary( conn )


def resolve_slot_times(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      window: tuple[ int, int ],
      duration_seconds: int,
      *,
      start_time: ScheduleTimeKey | None,
      itinerary_context: dict[ str, Any ] ) -> tuple[ tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None, ItinerarySaveResult | None ]:
   anchor_seconds, day_end_seconds = window
   itinerary = build_current_itinerary( saved_itinerary, **itinerary_context )
   blockers = collect_time_blocks_from_itinerary( itinerary )
   slot = resolve_schedule_slot(
      blockers,
      anchor_seconds,
      duration_seconds,
      day_end_seconds,
      start_time=start_time )

   if slot is None:
      error_type = (
         ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE
         if start_time is not None
         else ItineraryErrorType.NO_AVAILABLE_SLOT )

      return None, build_save_result(
         conn,
         error_type,
         **itinerary_context )

   return slot, None


def resolve_slot_times_allowing_visit_extension(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      visit_window: tuple[ int, int ],
      duration_seconds: int,
      *,
      start_time: ScheduleTimeKey | None,
      itinerary_context: dict[ str, Any ],
   ) -> tuple[ tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None, ItinerarySaveResult | None ]:
   """Prefer the guest visit window; if full, search zoo hours near existing schedule."""
   slot, slot_error = resolve_slot_times(
      conn,
      saved_itinerary,
      visit_window,
      duration_seconds,
      start_time=start_time,
      itinerary_context=itinerary_context )

   if slot_error is None:
      return slot, None

   if slot_error.status not in (
         ItineraryErrorType.NO_AVAILABLE_SLOT,
         ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE ):
      return None, slot_error

   zoo_hours_window = prepare_zoo_hours_schedule_window(
      conn,
      saved_itinerary,
      ensure_arrival_at_zoo_open=False,
      **itinerary_context )

   if isinstance( zoo_hours_window, ItinerarySaveResult ):
      return None, slot_error

   if zoo_hours_window.window == visit_window:
      return None, slot_error

   if start_time is not None:
      return resolve_slot_times(
         conn,
         saved_itinerary,
         zoo_hours_window.window,
         duration_seconds,
         start_time=start_time,
         itinerary_context=itinerary_context )

   slot = _resolve_extension_slot_before_or_after_visit(
      saved_itinerary,
      visit_window=visit_window,
      zoo_hours_window=zoo_hours_window.window,
      duration_seconds=duration_seconds,
      itinerary_context=itinerary_context )

   if slot is None:
      return None, slot_error

   return slot, None


def _resolve_extension_slot_before_or_after_visit(
      saved_itinerary: SavedItinerary,
      *,
      visit_window: tuple[ int, int ],
      zoo_hours_window: tuple[ int, int ],
      duration_seconds: int,
      itinerary_context: dict[ str, Any ],
   ) -> tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None:
   """After the visit window is full, try duration before arrival, then after departure."""
   itinerary = build_current_itinerary( saved_itinerary, **itinerary_context )
   blockers = collect_time_blocks_from_itinerary( itinerary )
   day_start_seconds, day_end_seconds = zoo_hours_window
   arrival_seconds, departure_seconds = visit_window

   return find_available_slot_before_or_after_bounds(
      blockers,
      duration_seconds,
      day_start_seconds=day_start_seconds,
      day_end_seconds=day_end_seconds,
      before_end_seconds=arrival_seconds,
      after_start_seconds=departure_seconds )


def effective_duration_seconds(
      duration_minutes: int | None,
      default_duration_seconds: int | None ) -> int | None:
   if default_duration_seconds is None:
      return None

   if duration_minutes is not None:
      return duration_minutes_to_seconds( duration_minutes )

   return default_duration_seconds
