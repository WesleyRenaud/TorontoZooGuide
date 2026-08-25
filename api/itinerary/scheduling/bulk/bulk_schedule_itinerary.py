from __future__ import annotations

from ....animals.coordinators.animal_coordinator import AnimalCoordinator
from .attraction_covered_animals import apply_covered_by_attraction_schedules
from ....attractions.coordinators.attraction_coordinator import AttractionCoordinator
from .bulk_schedule_finalize import finalize_bulk_schedule_itinerary
from .bulk_schedule_loop_packing import pack_stops_into_bulk_schedule
from .bulk_schedule_transit_legs import apply_bulk_schedule_transit_legs
from .bulk_schedule_window_prep import itinerary_has_items_to_rebuild
from .bulk_schedule_window_prep import prepare_bulk_schedule_windows
from ..core.guest_item_schedule_status import has_itinerary_schedule_times
from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ....guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from .guardians_talk_covered_animals import apply_covered_by_talk_schedules
from ..items.schedule_itinerary_helpers import build_itinerary_context
from ..items.schedule_itinerary_helpers import build_save_result
from ..items.schedule_itinerary_helpers import prepare_zoo_hours_schedule_window
from .loop_schedule_stop import LoopScheduleStop
from ...results.itinerary_save_result import ItinerarySaveResult
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ....wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def is_itinerary_animal_unscheduled( animal_row: ItineraryAnimalRecord ) -> bool:
   return not has_itinerary_schedule_times(
      animal_row.start_time,
      animal_row.end_time )


def bulk_schedule_itinerary(
      conn: Connection,
      *,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      visit_date_temp: float | None = None,
      confirming_fixed_time_item_long_wait: bool = False,
      animals_to_schedule: list[ ItineraryAnimalRecord ] | None = None,
      stops_to_schedule: list[ LoopScheduleStop ] | None = None ) -> ItinerarySaveResult:
   itinerary_context = build_itinerary_context(
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_coordinator=guardians_coordinator,
      wild_encounter_coordinator=wild_encounter_coordinator,
      visit_date_temp=visit_date_temp )

   if stops_to_schedule is None:
      stops_to_schedule = list( animals_to_schedule or [] )

   saved_itinerary = fetch_saved_itinerary( conn )

   # Rebuild may have no animal/attraction stops when the day only has talks or
   # encounters. Fail only when the itinerary itself has no items.
   if not stops_to_schedule and not itinerary_has_items_to_rebuild(
         saved_itinerary ):
      return build_save_result(
         conn,
         ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED,
         **itinerary_context )

   prepared_window = prepare_zoo_hours_schedule_window(
      conn,
      saved_itinerary,
      **itinerary_context )

   if isinstance( prepared_window, ItinerarySaveResult ):
      return prepared_window

   prep = prepare_bulk_schedule_windows(
      conn,
      prepared_window=prepared_window,
      itinerary_context=itinerary_context )
   packing = pack_stops_into_bulk_schedule(
      conn,
      prep=prep,
      stops_to_schedule=stops_to_schedule )

   if not packing.loop_units and not (
         packing.covered_by_talk or packing.covered_by_attraction ):
      return finalize_bulk_schedule_itinerary(
         conn,
         previous_itinerary=prep.previous_itinerary,
         itinerary_context=itinerary_context )

   apply_covered_by_talk_schedules( conn, packing.covered_by_talk )
   apply_covered_by_attraction_schedules( conn, packing.covered_by_attraction )
   apply_bulk_schedule_transit_legs( conn, prep=prep )

   return finalize_bulk_schedule_itinerary(
      conn,
      previous_itinerary=prep.previous_itinerary,
      itinerary_context=itinerary_context,
      remaining_stops=packing.remaining_stops )
