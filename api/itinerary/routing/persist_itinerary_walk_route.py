from __future__ import annotations

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from .build_itinerary_walk_route import build_itinerary_walk_route
from ..data_access.itinerary import fetch_saved_itinerary
from ..data_access.save_itinerary_walk_route import save_itinerary_walk_route
from ..domain.itinerary import build_current_itinerary
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ..scheduling.items.schedule_itinerary_helpers import build_itinerary_context
from ...types import Connection
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def rebuild_and_persist_itinerary_walk_route(
      conn: Connection,
      *,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      visit_date_temp: float | None = None ) -> bool:
   itinerary_context = build_itinerary_context(
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_coordinator=guardians_coordinator,
      wild_encounter_coordinator=wild_encounter_coordinator,
      visit_date_temp=visit_date_temp )
   saved_itinerary = fetch_saved_itinerary( conn )
   itinerary = build_current_itinerary(
      saved_itinerary,
      **itinerary_context )
   walk_route = build_itinerary_walk_route( itinerary )

   return save_itinerary_walk_route( conn, walk_route )
