from __future__ import annotations

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from .bulk.bulk_schedule_itinerary_runner import BulkScheduleItineraryRunner
from .bulk.bulk_schedule_stop_selector import BulkScheduleStopSelector
from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.saved_itinerary import SavedItinerary
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from .items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from .items.itinerary_schedule_context_builder import ItineraryScheduleContextBuilder
from ..results.itinerary_save_result import ItinerarySaveResult
from ...types import Types
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


class FixedTimeActivityRescheduler():
   @classmethod
   def reschedule_after_add(
         cls,
         conn: Types.Connection,
         *,
         animal_coordinator: type[ AnimalCoordinator ],
         attraction_coordinator: type[ AttractionCoordinator ],
         guardians_coordinator: type[ GuardiansCoordinator ],
         wild_encounter_coordinator: type[ WildEncounterCoordinator ],
         visit_date_temp: float | None = None,
         saved_itinerary_before_clear: SavedItinerary | None ) -> ItinerarySaveResult:
      itinerary_context = ItineraryScheduleContextBuilder.build(
         animal_coordinator=animal_coordinator,
         attraction_coordinator=attraction_coordinator,
         guardians_coordinator=guardians_coordinator,
         wild_encounter_coordinator=wild_encounter_coordinator,
         visit_date_temp=visit_date_temp )
      stops_to_schedule = BulkScheduleStopSelector.stops_matching_previous(
         saved_itinerary_before_clear,
         ItineraryProvider.fetch_saved_itinerary( conn ) )

      if not stops_to_schedule:
         return ItinerarySaveResultBuilder.success_result( conn, **itinerary_context )

      return BulkScheduleItineraryRunner.run(
         conn,
         stops_to_schedule=stops_to_schedule,
         confirming_fixed_time_item_long_wait=True,
         **itinerary_context )
