from __future__ import annotations

from typing import Any

from ....animals.coordinators.animal_coordinator import AnimalCoordinator
from ....attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..core.resolve_schedule_slot import resolve_schedule_slot
from ..core.scheduling_anchor import scheduling_anchor_seconds
from ..core.scheduling_anchor import scheduling_day_end_seconds
from ..core.time_block import collect_time_blocks_from_itinerary
from ...data_access.itinerary import fetch_itinerary_date
from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.saved_itinerary import SavedItinerary
from ....guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ...logic.itinerary import build_current_itinerary
from ...logic.itinerary_result_reason import ItineraryResultReason
from ...logic.itinerary_save_result import ItinerarySaveResult
from ....shared.duration_values import duration_minutes_to_seconds
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ....types import ScheduleTimeKey
from ....wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from ....zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record


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
      suppressed_warnings: tuple[ ItineraryErrorType, ... ] = (),
      **itinerary_context: Any ) -> ItinerarySaveResult:
   return ItinerarySaveResult(
      suppressed_warnings=suppressed_warnings,
      itinerary=build_current_itinerary(
         fetch_saved_itinerary( conn ),
         **itinerary_context ) )


def resolve_schedule_window(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      **itinerary_context: Any ) -> tuple[ int, int ] | ItinerarySaveResult:
   visit_date = fetch_itinerary_date( conn )

   if visit_date is None:
      return build_save_result(
         conn,
         ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         **itinerary_context )

   zoo_hours_record = fetch_zoo_hours_record( conn, visit_date )

   anchor_seconds = scheduling_anchor_seconds(
      zoo_hours_record,
      saved_itinerary.arrival_time )
   day_end_seconds = scheduling_day_end_seconds(
      zoo_hours_record,
      saved_itinerary.departure_time )

   if anchor_seconds is None or day_end_seconds is None:
      return build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_context )

   return ( anchor_seconds, day_end_seconds )


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


def effective_duration_seconds(
      duration_minutes: int | None,
      default_duration_seconds: int | None ) -> int | None:
   if default_duration_seconds is None:
      return None

   if duration_minutes is not None:
      return duration_minutes_to_seconds( duration_minutes )

   return default_duration_seconds
