from __future__ import annotations

from typing import Any

from ....animals.coordinators.animal_coordinator import AnimalCoordinator
from ....attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ....guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ....wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


class ItineraryScheduleContextBuilder():
   @classmethod
   def build(
         cls,
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
