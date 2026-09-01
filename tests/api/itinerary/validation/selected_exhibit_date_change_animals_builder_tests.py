from __future__ import annotations

from datetime import date

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.validation.selected_exhibit_date_change_animals_builder import SelectedExhibitDateChangeAnimalsBuilder
from api.models.animal import Animal
from api.models.animal_diff import AnimalDiff
from api.shared.constants import Constants


AFRICA_SAVANNA = 'Africa Savanna'
AMERICAS = 'Americas Outdoor Mayan Temple Ruins'


def _animal(
      *,
      species: str,
      exhibit: str,
      likelihood: int,
      enclosure_name: str | None = None ) -> Animal:
   return Animal(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name,
      likelihood=likelihood )


def _animal_diff(
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None,
      is_added: bool = False,
      old_likelihood: int | None = None,
      new_likelihood: int | None = None ) -> AnimalDiff:
   return AnimalDiff(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name,
      old_likelihood=old_likelihood,
      new_likelihood=new_likelihood,
      is_added=is_added )


def _viewable_animals_by_date() -> dict[ date, list[ Animal ] ]:
   return {
      date( 2026, 1, 15 ): [
         _animal(
            species='African Lion',
            exhibit=AFRICA_SAVANNA,
            likelihood=100 ),
         _animal(
            species='Spotted Hyena',
            exhibit=AFRICA_SAVANNA,
            likelihood=30 ),
      ],
      date( 2026, 6, 15 ): [
         _animal(
            species='African Lion',
            exhibit=AFRICA_SAVANNA,
            likelihood=100 ),
         _animal(
            species='Spotted Hyena',
            exhibit=AFRICA_SAVANNA,
            likelihood=80 ),
      ],
      date( 2026, 10, 17 ): [
         _animal(
            species='African Lion',
            exhibit=AFRICA_SAVANNA,
            likelihood=100 ),
      ],
      date( 2026, 10, 31 ): [
         _animal(
            species='African Lion',
            exhibit=AFRICA_SAVANNA,
            likelihood=100 ),
         _animal(
            species='Capybara',
            exhibit=AMERICAS,
            likelihood=90 ),
      ],
   }


@pytest.fixture
def stub_selected_exhibit_animal_coordinator(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   animals_by_date = _viewable_animals_by_date()

   def get_animals_viewable_on_day(
         *,
         day: int,
         month: int | str,
         year: int,
         temp: float | None,
         include_off_display_animals: bool,
         for_itinerary: bool,
         threshold: int | None = None,
         exhibits_to_include: list[ str ] | None = None ) -> list[ Animal ]:
      visit_date = date(
         year,
         int( month ) if isinstance( month, str ) else month,
         day )
      animals = animals_by_date.get( visit_date, [] )

      if exhibits_to_include:
         animals = [
            animal
            for animal in animals
            if animal.exhibit in exhibits_to_include
         ]

      if threshold is not None:
         animals = [
            animal
            for animal in animals
            if ( animal.likelihood or 0 ) >= threshold
         ]

      return animals

   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_viewable_on_day',
      get_animals_viewable_on_day )


def Test_ApplyOnDateChange_TestContinuingSelectedExhibit_ExpectAddedAnimalsFlagged(
      stub_selected_exhibit_animal_coordinator: None ) -> None:
   animals = SelectedExhibitDateChangeAnimalsBuilder.apply_on_date_change(
      AnimalCoordinator,
      existing_animals=[
         _animal_diff(
            species='African Lion',
            exhibit=AFRICA_SAVANNA,
            new_likelihood=100 ),
      ],
      selected_exhibits=[ AFRICA_SAVANNA ],
      previously_selected_exhibits=[ AFRICA_SAVANNA ],
      saved_animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit=AFRICA_SAVANNA,
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
      visit_date=date( 2026, 6, 15 ),
      old_visit_date=date( 2026, 1, 15 ),
      visit_date_temp=28 )

   added_animals = [
      animal
      for animal in animals
      if animal.is_added
   ]
   lion = next(
      animal
      for animal in animals
      if animal.species == 'African Lion' )

   assert added_animals
   assert all(
      ( animal.new_likelihood or 0 ) >= Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD
      for animal in added_animals )
   hyena = next(
      animal
      for animal in added_animals
      if animal.species == 'Spotted Hyena' )
   assert hyena.old_likelihood == 30
   assert hyena.old_likelihood < ( hyena.new_likelihood or 0 )
   assert lion.is_added is False


def Test_ApplyOnDateChange_TestNewlySelectedExhibit_ExpectNoAddedFlag(
      stub_selected_exhibit_animal_coordinator: None ) -> None:
   animals = SelectedExhibitDateChangeAnimalsBuilder.apply_on_date_change(
      AnimalCoordinator,
      existing_animals=[
         _animal_diff(
            species='African Lion',
            exhibit=AFRICA_SAVANNA,
            new_likelihood=100 ),
      ],
      selected_exhibits=[ AFRICA_SAVANNA, AMERICAS ],
      previously_selected_exhibits=[ AFRICA_SAVANNA ],
      saved_animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit=AFRICA_SAVANNA,
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
      visit_date=date( 2026, 10, 31 ),
      old_visit_date=date( 2026, 10, 17 ),
      visit_date_temp=5 )

   americas_animals = [
      animal
      for animal in animals
      if animal.exhibit == AMERICAS
   ]

   assert americas_animals
   assert all( animal.is_added is False for animal in americas_animals )
   assert all(
      ( animal.new_likelihood or 0 ) >= Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD
      for animal in americas_animals )


def Test_ApplyOnDateChange_TestFrontendRebuiltAnimals_ExpectContinuingExhibitFlagged(
      stub_selected_exhibit_animal_coordinator: None ) -> None:
   animals = SelectedExhibitDateChangeAnimalsBuilder.apply_on_date_change(
      AnimalCoordinator,
      existing_animals=[
         _animal_diff(
            species='African Lion',
            exhibit=AFRICA_SAVANNA,
            new_likelihood=100 ),
         _animal_diff(
            species='Southern White Rhinoceros',
            exhibit=AFRICA_SAVANNA,
            new_likelihood=100 ),
         _animal_diff(
            species='River Hippopotamus',
            exhibit=AFRICA_SAVANNA,
            new_likelihood=100 ),
      ],
      selected_exhibits=[ AFRICA_SAVANNA ],
      previously_selected_exhibits=[ AFRICA_SAVANNA ],
      saved_animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit=AFRICA_SAVANNA,
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
      visit_date=date( 2026, 10, 17 ),
      old_visit_date=date( 2026, 10, 31 ),
      visit_date_temp=18 )

   by_species = { animal.species: animal for animal in animals }

   assert by_species[ 'Southern White Rhinoceros' ].is_added is True
   assert by_species[ 'River Hippopotamus' ].is_added is True
   assert by_species[ 'African Lion' ].is_added is False


def Test_ApplyOnDateChange_TestDeselectedExhibit_ExpectAmericasAnimalsOmitted(
      stub_selected_exhibit_animal_coordinator: None ) -> None:
   animals = SelectedExhibitDateChangeAnimalsBuilder.apply_on_date_change(
      AnimalCoordinator,
      existing_animals=[
         _animal_diff(
            species='African Lion',
            exhibit=AFRICA_SAVANNA,
            new_likelihood=100 ),
      ],
      selected_exhibits=[ AFRICA_SAVANNA ],
      previously_selected_exhibits=[ AFRICA_SAVANNA, AMERICAS ],
      saved_animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit=AFRICA_SAVANNA,
            old_likelihood=None,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='Capybara',
            exhibit=AMERICAS,
            old_likelihood=None,
            new_likelihood=90,
         ),
      ],
      visit_date=date( 2026, 10, 17 ),
      old_visit_date=date( 2026, 10, 31 ),
      visit_date_temp=18 )

   assert all(
      animal.exhibit != AMERICAS
      for animal in animals )
