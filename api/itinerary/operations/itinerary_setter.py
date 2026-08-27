from __future__ import annotations

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..conflicts.itinerary_save_restrictive_hours_adjuster import ItinerarySaveRestrictiveHoursAdjuster
from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.itinerary_save_input_mapper import ItinerarySaveInputMapper
from ..data_access.itinerary_transportation_input import ItineraryTransportationInput
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from .itinerary_save_committer import ItinerarySaveCommitter
from .itinerary_save_context_builder import ItinerarySaveContextBuilder
from .itinerary_save_context_preparer import ItinerarySaveContextPreparer
from .itinerary_save_warning_checker import ItinerarySaveWarningChecker
from .itinerary_save_zoo_hours_validator import ItinerarySaveZooHoursValidator
from ..results.itinerary_save_result import ItinerarySaveResult
from ...types import Connection, DateInput, TimeInput
from ..wild_encounter_item_key import WildEncounterScheduleItemKey
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


class ItinerarySetter():
   @classmethod
   def set(
         cls,
         conn: Connection,
         date: DateInput,
         arrival_time: TimeInput,
         departure_time: TimeInput,
         selected_exhibits: list[ str ] | None = None,
         animals: list[ dict[ str, str ] ] | None = None,
         attractions: list[ str ] | None = None,
         guardians_talks: list[ dict[ str, str | None ] ] | None = None,
         wild_encounters: list[ WildEncounterScheduleItemKey ] | None = None,
         transportations: list[ ItineraryTransportationInput ] | None = None,
         visit_date_temp: float | None = None,
         *,
         animal_coordinator: type[ AnimalCoordinator ],
         attraction_coordinator: type[ AttractionCoordinator ],
         guardians_coordinator: type[ GuardiansCoordinator ],
         wild_encounter_coordinator: type[ WildEncounterCoordinator ],
         overriding_conflicting_guardians_talks: bool = False,
         confirming_short_visit: bool = False,
         confirming_early_admission: bool = False,
         confirming_guardians_talk_unschedule: bool,
         confirming_wild_encounter_unschedule: bool,
         confirming_fixed_time_item_long_wait: bool = False,
         confirming_guardians_talk_without_animal: bool = False,
         confirming_attraction_without_animal: bool = False ) -> ItinerarySaveResult:
      save_input = ItinerarySaveInputMapper.map_itinerary_save_input(
         date,
         arrival_time,
         departure_time,
         selected_exhibits,
         animals,
         attractions,
         guardians_talks,
         wild_encounters,
         transportations )
      old_visit_date = ItineraryProvider.fetch_itinerary_date( conn )

      controller_kwargs = ItinerarySaveContextBuilder.controller_kwargs(
         animal_coordinator=animal_coordinator,
         attraction_coordinator=attraction_coordinator,
         guardians_coordinator=guardians_coordinator,
         wild_encounter_coordinator=wild_encounter_coordinator,
         visit_date_temp=visit_date_temp )
      save_input, adjustments = ItinerarySaveRestrictiveHoursAdjuster.adjust(
         conn,
         save_input,
         old_visit_date=old_visit_date )

      zoo_hours_error = ItinerarySaveZooHoursValidator.validate(
         conn,
         save_input,
         controller_kwargs )

      if zoo_hours_error is not None:
         return zoo_hours_error

      context = ItinerarySaveContextPreparer.prepare(
         conn,
         save_input,
         old_visit_date=old_visit_date,
         animal_coordinator=animal_coordinator,
         attraction_coordinator=attraction_coordinator,
         guardians_coordinator=guardians_coordinator,
         wild_encounter_coordinator=wild_encounter_coordinator,
         visit_date_temp=visit_date_temp,
         itinerary_controller_kwargs=controller_kwargs,
         adjustments=adjustments )

      context, save_warning = ItinerarySaveWarningChecker.check(
         context,
         confirming_short_visit=confirming_short_visit,
         confirming_early_admission=confirming_early_admission,
         confirming_guardians_talk_unschedule=confirming_guardians_talk_unschedule,
         confirming_wild_encounter_unschedule=confirming_wild_encounter_unschedule,
         confirming_fixed_time_item_long_wait=confirming_fixed_time_item_long_wait,
         confirming_guardians_talk_without_animal=(
            confirming_guardians_talk_without_animal ),
         confirming_attraction_without_animal=(
            confirming_attraction_without_animal ),
         overriding_conflicting_guardians_talks=(
            overriding_conflicting_guardians_talks ) )

      if save_warning is not None:
         return save_warning

      return ItinerarySaveCommitter.commit(
         context,
         overriding_conflicting_guardians_talks=(
            overriding_conflicting_guardians_talks ) )
