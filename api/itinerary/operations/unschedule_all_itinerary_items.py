from __future__ import annotations

from typing import Any

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.itinerary_provider import ItineraryProvider
from ..domain.itinerary_builder import ItineraryBuilder
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from ..scheduling.items.itinerary_schedule_context_builder import ItineraryScheduleContextBuilder
from ..scheduling.unscheduling.guest_scheduled_itinerary_item_checker import GuestScheduledItineraryItemChecker
from ..scheduling.unscheduling.itinerary_schedule_clearer import ItineraryScheduleClearer
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
   itinerary_context: dict[ str, Any ] = ItineraryScheduleContextBuilder.build(
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_coordinator=guardians_coordinator,
      wild_encounter_coordinator=wild_encounter_coordinator,
      visit_date_temp=visit_date_temp )

   saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )

   if not GuestScheduledItineraryItemChecker.has_items( saved_itinerary ):
      return ItinerarySaveResultBuilder.save_result(
         conn,
         ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED,
         **itinerary_context )

   ItineraryScheduleClearer.clear_all( conn )

   return ItinerarySaveResult(
      itinerary=ItineraryBuilder.build_current(
         ItineraryProvider.fetch_saved_itinerary( conn ),
         **itinerary_context ) )
