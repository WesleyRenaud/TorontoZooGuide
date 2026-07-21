from __future__ import annotations

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...animals.search.animals_matching_query import species_exhibit_key_from_values
from ...animals.search.animals_matching_query import viewing_spot_key
from ..data_access.itinerary_animal_record import ItineraryAnimalRecord
from ..data_access.itinerary_save_input_mapper import map_named_strings
from ...models import Animal
from ...models import AnimalDiff
from ...shared.calendar_dates import DateValues
from ...shared.constants import ITINERARY_ANIMAL_MIN_LIKELIHOOD
from ...shared.value_conversion import ValueConversion
from ...types import DateInput


def _likelihoods_by_viewing_spot_for_exhibits(
      animal_coordinator: type[ AnimalCoordinator ],
      *,
      selected_exhibits: list[ str ],
      visit_date: DateInput,
      visit_date_temp: float | None = None,
      threshold: int | None = None ) -> dict[ tuple[ str, str, str | None ], int | None ]:
   if not selected_exhibits:
      return {}

   parsed_date = DateValues.parse_date_value( visit_date )
   animals = animal_coordinator.get_animals_viewable_on_day(
      day=parsed_date.day,
      month=parsed_date.month,
      year=parsed_date.year,
      temp=visit_date_temp,
      include_off_display_animals=False,
      for_itinerary=True,
      threshold=threshold,
      exhibits_to_include=list( selected_exhibits ) )

   return {
      viewing_spot_key( animal ): animal.likelihood
      for animal in animals
      if animal.exhibit != None
   }


def _viewable_animals_for_exhibits(
      animal_coordinator: type[ AnimalCoordinator ],
      *,
      selected_exhibits: list[ str ],
      visit_date: DateInput,
      visit_date_temp: float | None = None,
      threshold: int | None = None ) -> list[ Animal ]:
   if not selected_exhibits:
      return []

   parsed_date = DateValues.parse_date_value( visit_date )

   return [
      animal
      for animal in animal_coordinator.get_animals_viewable_on_day(
         day=parsed_date.day,
         month=parsed_date.month,
         year=parsed_date.year,
         temp=visit_date_temp,
         include_off_display_animals=False,
         for_itinerary=True,
         threshold=threshold,
         exhibits_to_include=list( selected_exhibits ) )
      if animal.exhibit != None
   ]


def apply_selected_exhibit_animals_on_date_change(
      animal_coordinator: type[ AnimalCoordinator ],
      *,
      existing_animals: list[ AnimalDiff ],
      selected_exhibits: list[ str ],
      previously_selected_exhibits: list[ str ],
      saved_animal_rows: list[ ItineraryAnimalRecord ],
      visit_date: DateInput,
      old_visit_date: DateInput,
      visit_date_temp: float | None = None ) -> list[ AnimalDiff ]:
   """Sync exhibit animals for a date change.

   Only exhibits still selected on this save are considered. Animals from
   exhibits that remain selected (and were selected before) are flagged
   is_added when they newly meet the itinerary threshold. Newly selected
   exhibits contribute animals without that flag. Deselected exhibits are
   ignored.
   """
   selected = map_named_strings( selected_exhibits )
   previously_selected = set( map_named_strings( previously_selected_exhibits ) )
   continuing_exhibits = [
      exhibit
      for exhibit in selected
      if exhibit in previously_selected
   ]
   saved_animal_keys = {
      row.viewing_spot_key()
      for row in saved_animal_rows
   }
   saved_species_exhibit_keys = {
      row.species_exhibit_key()
      for row in saved_animal_rows
   }
   old_likelihoods = _likelihoods_by_viewing_spot_for_exhibits(
      animal_coordinator,
      selected_exhibits=continuing_exhibits,
      visit_date=old_visit_date,
      visit_date_temp=visit_date_temp )

   for animal in existing_animals:
      if animal.viewing_spot_key() in saved_animal_keys:
         continue

      if (
            species_exhibit_key_from_values( animal.species, animal.exhibit )
            in saved_species_exhibit_keys ):
         continue

      if animal.exhibit not in continuing_exhibits:
         continue

      animal.is_added = True

      if animal.old_likelihood is None:
         animal.old_likelihood = old_likelihoods.get( animal.viewing_spot_key() )

   animals = list( existing_animals )
   existing_keys = {
      animal.viewing_spot_key()
      for animal in animals
   }
   expand_old_likelihoods = _likelihoods_by_viewing_spot_for_exhibits(
      animal_coordinator,
      selected_exhibits=selected,
      visit_date=old_visit_date,
      visit_date_temp=visit_date_temp )

   for animal in _viewable_animals_for_exhibits(
         animal_coordinator,
         selected_exhibits=selected,
         visit_date=visit_date,
         visit_date_temp=visit_date_temp,
         threshold=ITINERARY_ANIMAL_MIN_LIKELIHOOD ):
      spot_key = viewing_spot_key( animal )

      if spot_key in existing_keys:
         continue

      enclosure_name = ValueConversion.as_nullable_string(
         animal.enclosure_name )
      animals.append(
         AnimalDiff(
            species=animal.species,
            exhibit=animal.exhibit,
            enclosure_name=enclosure_name,
            old_likelihood=expand_old_likelihoods.get( spot_key ),
            new_likelihood=animal.likelihood,
            is_added=animal.exhibit in previously_selected ) )
      existing_keys.add( spot_key )

   return animals
