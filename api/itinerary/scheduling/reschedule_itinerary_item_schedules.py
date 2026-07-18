from __future__ import annotations

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from .bulk.animals_for_bulk_schedule import stops_for_bulk_schedule
from .bulk.bulk_schedule_animals import bulk_schedule_animals
from ..data_access.saved_itinerary import SavedItinerary
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from .items.schedule_itinerary_helpers import build_itinerary_context
from .items.schedule_itinerary_helpers import build_success_result
from ..results.itinerary_save_result import ItinerarySaveResult
from ...types import Connection
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def reschedule_itinerary_items_after_fixed_time_activity_add(
      conn: Connection,
      *,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      visit_date_temp: float | None = None,
      saved_itinerary_before_clear: SavedItinerary | None ) -> ItinerarySaveResult:
   itinerary_context = build_itinerary_context(
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_coordinator=guardians_coordinator,
      wild_encounter_coordinator=wild_encounter_coordinator,
      visit_date_temp=visit_date_temp )
   stops_to_schedule = stops_for_bulk_schedule(
      saved_itinerary_before_clear,
      only_previously_scheduled=True )

   if not stops_to_schedule:
      return build_success_result( conn, **itinerary_context )

   return bulk_schedule_animals(
      conn,
      stops_to_schedule=stops_to_schedule,
      confirming_fixed_time_item_long_wait=True,
      **itinerary_context )
