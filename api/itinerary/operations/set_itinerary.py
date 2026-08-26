from __future__ import annotations

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from .check_set_itinerary_save_warnings import check_set_itinerary_save_warnings
from .commit_set_itinerary import commit_set_itinerary
from ..conflicts.itinerary_time_adjustments import adjust_set_itinerary_for_restrictive_hours
from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.itinerary_save_input_mapper import ItinerarySaveInputMapper
from ..data_access.itinerary_transportation_input import ItineraryTransportationInput
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from .prepare_set_itinerary_context import prepare_set_itinerary_context
from ..results.itinerary_save_result import ItinerarySaveResult
from .set_itinerary_context import itinerary_controller_kwargs
from ...types import Connection, DateInput, TimeInput
from .validate_set_itinerary_zoo_hours import validate_set_itinerary_zoo_hours
from ..wild_encounter_item_key import WildEncounterScheduleItemKey
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def set_itinerary(
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

   controller_kwargs = itinerary_controller_kwargs(
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_coordinator=guardians_coordinator,
      wild_encounter_coordinator=wild_encounter_coordinator,
      visit_date_temp=visit_date_temp )
   save_input, adjustments = adjust_set_itinerary_for_restrictive_hours(
      conn,
      save_input,
      old_visit_date=old_visit_date )

   zoo_hours_error = validate_set_itinerary_zoo_hours(
      conn,
      save_input,
      controller_kwargs )

   if zoo_hours_error is not None:
      return zoo_hours_error

   context = prepare_set_itinerary_context(
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

   context, save_warning = check_set_itinerary_save_warnings(
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

   return commit_set_itinerary(
      context,
      overriding_conflicting_guardians_talks=(
         overriding_conflicting_guardians_talks ) )
