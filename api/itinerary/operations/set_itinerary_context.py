from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..conflicts.itinerary_unschedule_confirmations import ItineraryUnscheduleRequirements
from ..data_access.itinerary import fetch_saved_itinerary
from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from ..domain.itinerary import build_current_itinerary
from ..domain.itinerary_adjustment import ItineraryAdjustment
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ...models import Itinerary
from ..results.itinerary_save_result import ItinerarySaveResult
from ...shared.enums import ItineraryErrorType
from ...types import Connection
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


@dataclass( frozen=True )
class SetItineraryContext:
   conn: Connection
   save_input: ItinerarySaveInput
   validated_itinerary: ValidatedItinerary
   current_itinerary: Itinerary
   saved_itinerary: SavedItinerary | None
   unschedule_requirements: ItineraryUnscheduleRequirements
   itinerary_controller_kwargs: dict[ str, Any ]
   adjustments: tuple[ ItineraryAdjustment, ... ] = ()
   suppressed_warnings: tuple[ ItineraryErrorType, ... ] = ()


def itinerary_controller_kwargs(
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


def build_set_itinerary_current_itinerary(
      conn: Connection,
      itinerary_controller_kwargs: dict[ str, Any ] ) -> Itinerary:
   return build_current_itinerary(
      fetch_saved_itinerary( conn ),
      **itinerary_controller_kwargs )


def build_set_itinerary_error_result(
      conn: Connection,
      status: ItineraryErrorType,
      itinerary_controller_kwargs: dict[ str, Any ],
      *,
      suppressed_warnings: tuple[ ItineraryErrorType, ... ] = () ) -> ItinerarySaveResult:
   return ItinerarySaveResult(
      status=status,
      suppressed_warnings=suppressed_warnings,
      itinerary=build_set_itinerary_current_itinerary(
         conn,
         itinerary_controller_kwargs ) )
