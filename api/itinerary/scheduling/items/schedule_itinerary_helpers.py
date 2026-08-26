from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from ....animals.coordinators.animal_coordinator import AnimalCoordinator
from ....attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..core.find_next_available_slot import find_available_slot_before_or_after_bounds
from ..core.resolve_schedule_slot import resolve_schedule_slot
from ..core.scheduling_anchor import scheduling_anchor_seconds_covering_fixed_zoo_starts
from ..core.scheduling_anchor import scheduling_day_end_seconds
from ..core.time_block import collect_time_blocks_from_itinerary
from ...data_access.itinerary_provider import ItineraryProvider
from ...data_access.itinerary_status_provider import ItineraryStatusProvider
from ...data_access.saved_itinerary import SavedItinerary
from ...domain.itinerary import build_current_itinerary
from ...domain.itinerary_adjustment import ItineraryAdjustment
from ....guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ...results.itinerary_result_reason import ItineraryResultReason
from ...results.itinerary_save_result import ItinerarySaveResult
from ....shared.calendar_dates import DateValues
from ....shared.duration_values import duration_minutes_to_seconds
from ....shared.enums import ItineraryErrorType
from ....shared.operating_hours import OperatingHours
from ....types import Connection
from ....types import ScheduleTimeKey
from ...validation.fixed_zoo_schedule_start_times import fixed_zoo_schedule_start_times_from_saved_itinerary
from ....wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from ....zoo_hours.data_access.zoo_hours_provider import ZooHoursProvider
from ....zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


@dataclass( frozen=True )
class PreparedScheduleWindow:
   saved_itinerary: SavedItinerary
   window: tuple[ int, int ]
   visit_date: date
   zoo_operating_hours: OperatingHours | None = None


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
      reasons: list[ ItineraryResultReason ] | None = None,
      suppressed_warnings: list[ ItineraryErrorType ] | None = None,
      **itinerary_context: Any ) -> ItinerarySaveResult:
   return ItinerarySaveResult(
      status=status,
      reasons=reasons or [],
      suppressed_warnings=suppressed_warnings or [],
      itinerary=build_current_itinerary(
         ItineraryProvider.fetch_saved_itinerary( conn ),
         **itinerary_context ) )


def build_success_result(
      conn: Connection,
      *,
      adjustments: list[ ItineraryAdjustment ] | None = None,
      suppressed_warnings: list[ ItineraryErrorType ] | None = None,
      **itinerary_context: Any ) -> ItinerarySaveResult:
   return ItinerarySaveResult(
      adjustments=adjustments or [],
      suppressed_warnings=suppressed_warnings or [],
      itinerary=build_current_itinerary(
         ItineraryProvider.fetch_saved_itinerary( conn ),
         **itinerary_context ) )


def persist_itinerary_walk_route(
      conn: Connection,
      **itinerary_context: Any ) -> None:
   from ...routing.persist_itinerary_walk_route import rebuild_and_persist_itinerary_walk_route

   rebuild_and_persist_itinerary_walk_route( conn, **itinerary_context )


def prepare_schedule_window(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      **itinerary_context: Any ) -> PreparedScheduleWindow | ItinerarySaveResult:
   visit_date = ItineraryProvider.fetch_itinerary_date( conn )

   if visit_date is None:
      return build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_context )

   parsed_visit_date = DateValues.parse_date_value( visit_date )

   if parsed_visit_date is None:
      return build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_context )

   zoo_hours_record = ZooHoursProvider.fetch_zoo_hours_record( conn, visit_date )
   zoo_operating_hours_value = (
      None
      if zoo_hours_record is None
      else zoo_hours_record.operating_hours() )
   allow_early_admission = _early_admission_scheduling_is_allowed( conn )

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
      window=( anchor_seconds, day_end_seconds ),
      visit_date=parsed_visit_date,
      zoo_operating_hours=zoo_operating_hours_value )


def prepare_zoo_hours_schedule_window(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      **itinerary_context: Any ) -> PreparedScheduleWindow | ItinerarySaveResult:
   visit_date = ItineraryProvider.fetch_itinerary_date( conn )

   if visit_date is None:
      return build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_context )

   parsed_visit_date = DateValues.parse_date_value( visit_date )

   if parsed_visit_date is None:
      return build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_context )

   zoo_hours_record = ZooHoursProvider.fetch_zoo_hours_record( conn, visit_date )
   zoo_operating_hours_value = (
      None
      if zoo_hours_record is None
      else zoo_hours_record.operating_hours() )
   allow_early_admission = _early_admission_scheduling_is_allowed( conn )

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
      window=window,
      visit_date=parsed_visit_date,
      zoo_operating_hours=zoo_operating_hours_value )


def zoo_hours_schedule_window_seconds(
      zoo_hours_record: ZooHoursRecord | None,
      *,
      fixed_zoo_start_times: list[ ScheduleTimeKey ] | None = None,
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
   return ItineraryStatusProvider.is_itinerary_error_suppressed(
      conn,
      ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP )


def resolve_slot_times(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      window: tuple[ int, int ],
      duration_seconds: int,
      *,
      start_time: ScheduleTimeKey | None,
      itinerary_context: dict[ str, Any ],
      earliest_start_seconds: int | None = None ) -> tuple[ tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None, ItinerarySaveResult | None ]:
   anchor_seconds, day_end_seconds = window

   if earliest_start_seconds is not None:
      anchor_seconds = max( anchor_seconds, earliest_start_seconds )

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
      day_hours_window: tuple[ int, int ] | None = None,
      earliest_start_seconds: int | None = None,
   ) -> tuple[ tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None, ItinerarySaveResult | None ]:
   """Prefer the guest visit window; if full, search day hours near existing schedule."""
   slot, slot_error = resolve_slot_times(
      conn,
      saved_itinerary,
      visit_window,
      duration_seconds,
      start_time=start_time,
      itinerary_context=itinerary_context,
      earliest_start_seconds=earliest_start_seconds )

   if slot_error is None:
      return slot, None

   if slot_error.status not in (
         ItineraryErrorType.NO_AVAILABLE_SLOT,
         ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE ):
      return None, slot_error

   if day_hours_window is None:
      prepared_day_hours = prepare_zoo_hours_schedule_window(
         conn,
         saved_itinerary,
         **itinerary_context )

      if isinstance( prepared_day_hours, ItinerarySaveResult ):
         return None, slot_error

      day_hours_window = prepared_day_hours.window

   if day_hours_window == visit_window:
      return None, slot_error

   if start_time is not None:
      return resolve_slot_times(
         conn,
         saved_itinerary,
         day_hours_window,
         duration_seconds,
         start_time=start_time,
         itinerary_context=itinerary_context,
         earliest_start_seconds=earliest_start_seconds )

   slot = _resolve_extension_slot_before_or_after_visit(
      saved_itinerary,
      visit_window=visit_window,
      day_hours_window=day_hours_window,
      duration_seconds=duration_seconds,
      itinerary_context=itinerary_context )

   if slot is None:
      return None, slot_error

   return slot, None


def _resolve_extension_slot_before_or_after_visit(
      saved_itinerary: SavedItinerary,
      *,
      visit_window: tuple[ int, int ],
      day_hours_window: tuple[ int, int ],
      duration_seconds: int,
      itinerary_context: dict[ str, Any ],
   ) -> tuple[ ScheduleTimeKey, ScheduleTimeKey ] | None:
   """After the visit window is full, try duration before arrival, then after departure."""
   itinerary = build_current_itinerary( saved_itinerary, **itinerary_context )
   blockers = collect_time_blocks_from_itinerary( itinerary )
   day_start_seconds, day_end_seconds = day_hours_window
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
