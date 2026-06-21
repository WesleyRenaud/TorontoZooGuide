from __future__ import annotations

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from .bulk.bulk_schedule_animals import bulk_schedule_animals
from ..data_access.unschedule_itinerary_item import clear_all_itinerary_animal_schedules
from ..data_access.unschedule_itinerary_item import clear_all_itinerary_attraction_schedules
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ..results.itinerary_save_result import ItinerarySaveResult
from ...types import Connection
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def clear_all_itinerary_item_schedules( conn: Connection ) -> None:
   cur = conn.cursor()

   try:
      clear_all_itinerary_animal_schedules( cur )
      clear_all_itinerary_attraction_schedules( cur )
      conn.commit()

   finally:
      cur.close()


def reschedule_itinerary_items_after_fixed_time_activity_add(
      conn: Connection,
      *,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      visit_date_temp: float | None = None ) -> ItinerarySaveResult:
   clear_all_itinerary_item_schedules( conn )

   return bulk_schedule_animals(
      conn,
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_coordinator=guardians_coordinator,
      wild_encounter_coordinator=wild_encounter_coordinator,
      visit_date_temp=visit_date_temp )
