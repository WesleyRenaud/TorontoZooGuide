from __future__ import annotations

from dataclasses import replace

from ...animals.controllers.animal_controller import AnimalController
from ...animals.logic.animals_matching_query import species_exhibit_key_from_values
from ...attractions.controllers.attraction_controller import AttractionController
from ..data_access.clear_itinerary import clear_itinerary
from ..data_access.itinerary import fetch_itinerary_date
from ..data_access.itinerary import fetch_saved_itinerary
from ..data_access.itinerary_animal_input import ItineraryAnimalInput
from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..data_access.itinerary_save_input_mapper import map_itinerary_save_input
from ..data_access.save_itinerary import save_validated_itinerary
from ...guardians.controllers.guardians_controller import GuardiansController
from .guardians_talk_schedule_trimming import apply_guardians_talk_trimming
from .guardians_talk_unschedule_items import apply_guardians_talk_unschedule_to_validated_itinerary
from .guardians_talk_unschedule_warning import build_guardians_talk_unschedule_issue
from .guardians_talk_unschedule_warning import guardians_talks_requiring_unschedule
from .itinerary import build_current_itinerary
from .itinerary_arrival_time_validation import arrival_time_is_valid_for_zoo_hours
from .itinerary_departure_time_validation import departure_time_is_valid_for_zoo_hours
from .itinerary_save_result import ItinerarySaveResult
from .itinerary_validation import validate_itinerary_for_save
from ...shared.enums import ItineraryErrorType
from .short_visit_warning import apply_short_visit_warning_preferences
from .short_visit_warning import short_visit_warning_is_required
from ...types import Connection, DateInput, TimeInput
from .wild_encounter_time_conflicts import remove_scheduled_items_with_time_conflicts
from .wild_encounter_unschedule_items import apply_wild_encounter_unschedule_to_validated_itinerary
from .wild_encounter_unschedule_warning import build_wild_encounter_unschedule_issue
from .wild_encounter_unschedule_warning import wild_encounters_requiring_unschedule
from ...wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from ...zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record


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
      animal_controller: type[ AnimalController ],
      visit_date_temp: float | None = None ) -> tuple[ ItineraryAnimalInput, ... ]:
   if not save_input.selected_exhibits:
      return ()

   animals = animal_controller.get_animals_viewable_on_day(
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
      animal_controller: type[ AnimalController ],
      visit_date_temp: float | None = None ) -> ItinerarySaveInput:
   animals_from_selected_exhibits = build_itinerary_animal_inputs_from_selected_exhibits(
      save_input,
      animal_controller,
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
      animal_controller: type[ AnimalController ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      overriding_conflicting_guardians_talks: bool = False,
      confirming_short_visit: bool = False,
      suppress_short_visit_warning: bool = False,
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
      animal_controller,
      visit_date_temp=visit_date_temp )

   zoo_hours_record = fetch_zoo_hours_record( conn, save_input.date.isoformat() )

   if (
         save_input.arrival_time is not None
         and save_input.departure_time is not None
   ):
      arrival_time_error = arrival_time_is_valid_for_zoo_hours(
         save_input.arrival_time,
         zoo_hours_record,
         departure_time=save_input.departure_time )

      if arrival_time_error != ItineraryErrorType.SUCCESS:
         return ItinerarySaveResult(
            error_type=arrival_time_error,
            itinerary=build_current_itinerary(
               fetch_saved_itinerary( conn ),
               animal_controller,
               attraction_controller,
               guardians_controller,
               wild_encounter_controller,
               visit_date_temp=visit_date_temp ) )

      departure_time_error = departure_time_is_valid_for_zoo_hours(
         save_input.departure_time,
         zoo_hours_record,
         arrival_time=save_input.arrival_time )

      if departure_time_error != ItineraryErrorType.SUCCESS:
         return ItinerarySaveResult(
            error_type=departure_time_error,
            itinerary=build_current_itinerary(
               fetch_saved_itinerary( conn ),
               animal_controller,
               attraction_controller,
               guardians_controller,
               wild_encounter_controller,
               visit_date_temp=visit_date_temp ) )

   if (
         save_input.arrival_time is not None
         and save_input.departure_time is not None
         and short_visit_warning_is_required(
            conn,
            save_input.arrival_time,
            save_input.departure_time,
            confirming_short_visit=confirming_short_visit )
   ):
      return ItinerarySaveResult(
         error_type=ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
         itinerary=build_current_itinerary(
            fetch_saved_itinerary( conn ),
            animal_controller,
            attraction_controller,
            guardians_controller,
            wild_encounter_controller,
            visit_date_temp=visit_date_temp ) )

   apply_short_visit_warning_preferences(
      conn,
      suppress_short_visit_warning=suppress_short_visit_warning )

   validated_itinerary = validate_itinerary_for_save(
      conn,
      save_input,
      animal_controller,
      attraction_controller,
      guardians_controller,
      wild_encounter_controller,
      new_visit_date_temp=visit_date_temp,
      old_visit_date=old_visit_date )

   saved_itinerary = (
      fetch_saved_itinerary( conn )
      if old_visit_date is not None
      else None )

   if saved_itinerary is not None:
      talks_requiring_unschedule = guardians_talks_requiring_unschedule(
         saved_itinerary,
         validated_itinerary )

      if (
            talks_requiring_unschedule
            and not confirming_guardians_talk_unschedule ):
         return ItinerarySaveResult(
            error_type=ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
            issues=(
               build_guardians_talk_unschedule_issue(
                  talks_requiring_unschedule ),
            ),
            itinerary=build_current_itinerary(
               saved_itinerary,
               animal_controller,
               attraction_controller,
               guardians_controller,
               wild_encounter_controller,
               visit_date_temp=visit_date_temp ) )

      if talks_requiring_unschedule:
         validated_itinerary = apply_guardians_talk_unschedule_to_validated_itinerary(
            validated_itinerary,
            talks_requiring_unschedule )

      encounters_requiring_unschedule = wild_encounters_requiring_unschedule(
         saved_itinerary,
         validated_itinerary )

      if (
            encounters_requiring_unschedule
            and not confirming_wild_encounter_unschedule ):
         return ItinerarySaveResult(
            error_type=ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
            issues=(
               build_wild_encounter_unschedule_issue(
                  encounters_requiring_unschedule ),
            ),
            itinerary=build_current_itinerary(
               saved_itinerary,
               animal_controller,
               attraction_controller,
               guardians_controller,
               wild_encounter_controller,
               visit_date_temp=visit_date_temp ) )

      if encounters_requiring_unschedule:
         validated_itinerary = apply_wild_encounter_unschedule_to_validated_itinerary(
            validated_itinerary,
            encounters_requiring_unschedule )

   if overriding_conflicting_guardians_talks:
      trimmed_guardians_talks = apply_guardians_talk_trimming(
         validated_itinerary.guardians_talks,
         validated_itinerary.wild_encounters )
      validated_itinerary = replace(
         validated_itinerary,
         guardians_talks=trimmed_guardians_talks )

   guardians_talks, wild_encounters, issues = remove_scheduled_items_with_time_conflicts(
      validated_itinerary.guardians_talks,
      validated_itinerary.wild_encounters )
   validated_itinerary = replace(
      validated_itinerary,
      guardians_talks=guardians_talks,
      wild_encounters=wild_encounters )

   clear_itinerary( conn )
   save_validated_itinerary( conn, save_input.date, validated_itinerary )

   itinerary = build_current_itinerary(
      fetch_saved_itinerary( conn ),
      animal_controller,
      attraction_controller,
      guardians_controller,
      wild_encounter_controller,
      visit_date_temp=visit_date_temp )

   return ItinerarySaveResult(
      itinerary=itinerary,
      issues=issues )
