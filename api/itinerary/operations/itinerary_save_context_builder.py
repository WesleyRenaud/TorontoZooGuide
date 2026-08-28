from __future__ import annotations

from typing import Any

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.itinerary_provider import ItineraryProvider
from ..domain.itinerary_builder import ItineraryBuilder
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ...models import Itinerary
from ..results.itinerary_save_result import ItinerarySaveResult
from ...shared.enums import ItineraryErrorType
from ...types import Types
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


class ItinerarySaveContextBuilder():
   @classmethod
   def controller_kwargs(
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


   @classmethod
   def current_itinerary(
         cls,
         conn: Types.Connection,
         itinerary_controller_kwargs: dict[ str, Any ] ) -> Itinerary:
      return ItineraryBuilder.build_current(
         ItineraryProvider.fetch_saved_itinerary( conn ),
         **itinerary_controller_kwargs )


   @classmethod
   def error_result(
         cls,
         conn: Types.Connection,
         status: ItineraryErrorType,
         itinerary_controller_kwargs: dict[ str, Any ],
         *,
         suppressed_warnings: list[ ItineraryErrorType ] | None = None ) -> ItinerarySaveResult:
      return ItinerarySaveResult(
         status=status,
         suppressed_warnings=suppressed_warnings or [],
         itinerary=cls.current_itinerary(
            conn,
            itinerary_controller_kwargs ) )
