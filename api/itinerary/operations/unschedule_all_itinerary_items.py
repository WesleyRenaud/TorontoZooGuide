from __future__ import annotations

from typing import Any

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.itinerary_provider import ItineraryProvider
from ..domain.itinerary_builder import ItineraryBuilder
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.items.schedule_itinerary_helpers import build_itinerary_context
from ..scheduling.items.schedule_itinerary_helpers import build_save_result
from ..scheduling.unscheduling.clear_all_itinerary_schedules import clear_all_itinerary_schedules
from ..scheduling.unscheduling.guest_scheduled_itinerary_items import saved_itinerary_has_guest_scheduled_items
from ...shared.enums import ItineraryErrorType
from ...types import Connection
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def unschedule_all_itinerary_items(
      conn: Connection,
      *,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      visit_date_temp: float | None = None ) -> ItinerarySaveResult:
   itinerary_context: dict[ str, Any ] = build_itinerary_context(
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_coordinator=guardians_coordinator,
      wild_encounter_coordinator=wild_encounter_coordinator,
      visit_date_temp=visit_date_temp )

   saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )

   if not saved_itinerary_has_guest_scheduled_items( saved_itinerary ):
      return build_save_result(
         conn,
         ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED,
         **itinerary_context )

   clear_all_itinerary_schedules( conn )

   return ItinerarySaveResult(
      itinerary=ItineraryBuilder.build_current(
         ItineraryProvider.fetch_saved_itinerary( conn ),
         **itinerary_context ) )
