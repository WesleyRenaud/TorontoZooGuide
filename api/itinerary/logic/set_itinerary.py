from __future__ import annotations

from dataclasses import replace

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...animals.logic.animals_matching_query import species_exhibit_key_from_values
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.itinerary import fetch_itinerary_date
from ..data_access.itinerary_animal_input import ItineraryAnimalInput
from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..data_access.itinerary_save_input_mapper import map_itinerary_save_input
from ...guardians.controllers.guardians_controller import GuardiansController
from .itinerary_save_result import ItinerarySaveResult
from .itinerary_time_adjustments import adjust_set_itinerary_for_restrictive_hours
from .set_itinerary_flow import check_set_itinerary_save_warnings
from .set_itinerary_flow import commit_set_itinerary
from .set_itinerary_flow import itinerary_controller_kwargs
from .set_itinerary_flow import prepare_set_itinerary_context
from .set_itinerary_flow import validate_set_itinerary_zoo_hours
from ...types import Connection, DateInput, TimeInput
from ...wild_encounters.controllers.wild_encounter_controller import WildEncounterController


def itinerary_animal_input_key( animal: ItineraryAnimalInput ) -> tuple[ str, str ]:
   return species_exhibit_key_from_values( animal.species, animal.exhibit )


def merge_itinerary_animal_inputs(
      animals: tuple[ ItineraryAnimalInput, ... ],
      animals_from_selected_exhibits: tuple[ ItineraryAnimalInput, ... ] ) -> tuple[ ItineraryAnimalInput, ... ]:
   merged: list[ ItineraryAnimalInput ] = []
   seen: set[ tuple[ str, str ] ] = set()

   for animal in ( *animals, *animals_from_selected_exhibits ):
      key = itinerary_animal_input_key( animal )

      if key in seen:
         continue

      seen.add( key )
      merged.append( animal )

   return tuple( merged )


def build_itinerary_animal_inputs_from_selected_exhibits(
      save_input: ItinerarySaveInput,
      animal_coordinator: type[ AnimalCoordinator ],
      visit_date_temp: float | None = None ) -> tuple[ ItineraryAnimalInput, ... ]:
   if not save_input.selected_exhibits:
      return ()

   animals = animal_coordinator.get_animals_viewable_on_day(
      day=save_input.day(),
      month=save_input.month(),
      year=save_input.year(),
      temp=visit_date_temp,
      include_off_display_animals=False,
      threshold=0,
      exhibits_to_include=list( save_input.selected_exhibits ) )

   return tuple(
      ItineraryAnimalInput(
         species=animal.species,
         exhibit=animal.exhibit )
      for animal in animals
      if animal.exhibit != None
   )


def expand_selected_exhibit_animals(
      save_input: ItinerarySaveInput,
      animal_coordinator: type[ AnimalCoordinator ],
      visit_date_temp: float | None = None ) -> ItinerarySaveInput:
   animals_from_selected_exhibits = build_itinerary_animal_inputs_from_selected_exhibits(
      save_input,
      animal_coordinator,
      visit_date_temp=visit_date_temp )

   if not animals_from_selected_exhibits:
      return save_input

   original_animal_keys = {
      itinerary_animal_input_key( animal )
      for animal in save_input.animals
   }
   animals_from_selected_exhibits = tuple(
      replace(
         animal,
         is_added=itinerary_animal_input_key( animal ) not in original_animal_keys )
      for animal in animals_from_selected_exhibits
   )

   return replace(
      save_input,
      animals=merge_itinerary_animal_inputs(
         save_input.animals,
         animals_from_selected_exhibits ) )


def set_itinerary(
      conn: Connection,
      date: DateInput,
      arrival_time: TimeInput,
      departure_time: TimeInput,
      animals: list[ dict[ str, str ] ],
      attractions: list[ str ],
      guardians_talks: list[ dict[ str, str | None ] ],
      wild_encounters: list[ str ],
      selected_exhibits: list[ str ] | None = None,
      visit_date_temp: float | None = None,
      *,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      overriding_conflicting_guardians_talks: bool = False,
      confirming_short_visit: bool = False,
      confirming_early_admission: bool = False,
      confirming_guardians_talk_unschedule: bool,
      confirming_wild_encounter_unschedule: bool ) -> ItinerarySaveResult:
   save_input = map_itinerary_save_input(
      date,
      arrival_time,
      departure_time,
      animals,
      attractions,
      guardians_talks,
      wild_encounters,
      selected_exhibits )
   old_visit_date = fetch_itinerary_date( conn )
   save_input = expand_selected_exhibit_animals(
      save_input,
      animal_coordinator,
      visit_date_temp=visit_date_temp )

   controller_kwargs = itinerary_controller_kwargs(
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_controller=guardians_controller,
      wild_encounter_controller=wild_encounter_controller,
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
      guardians_controller=guardians_controller,
      wild_encounter_controller=wild_encounter_controller,
      visit_date_temp=visit_date_temp,
      itinerary_controller_kwargs=controller_kwargs,
      adjustments=adjustments )

   context, save_warning = check_set_itinerary_save_warnings(
      context,
      confirming_short_visit=confirming_short_visit,
      confirming_early_admission=confirming_early_admission,
      confirming_guardians_talk_unschedule=confirming_guardians_talk_unschedule,
      confirming_wild_encounter_unschedule=confirming_wild_encounter_unschedule,
      overriding_conflicting_guardians_talks=(
         overriding_conflicting_guardians_talks ) )

   if save_warning is not None:
      return save_warning

   return commit_set_itinerary(
      context,
      overriding_conflicting_guardians_talks=(
         overriding_conflicting_guardians_talks ) )
