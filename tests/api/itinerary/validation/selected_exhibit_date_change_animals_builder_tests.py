from __future__ import annotations

from datetime import date

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.validation.selected_exhibit_date_change_animals_builder import SelectedExhibitDateChangeAnimalsBuilder
from api.models.animal import Animal
from api.models.animal_diff import AnimalDiff
from api.shared.constants import Constants
from api.shared.enums.position import Position


AFRICA_SAVANNA = 'Africa Savanna'
AMERICAS = 'Americas Outdoor Mayan Temple Ruins'
AFRICAN_LION = 'African Lion'
SPOTTED_HYENA = 'Spotted Hyena'
CAPYBARA = 'Capybara'
SOUTHERN_WHITE_RHINOCEROS = 'Southern White Rhinoceros'
RIVER_HIPPOPOTAMUS = 'River Hippopotamus'
AFRICAN_PENGUIN = 'African Penguin'
OUTDOOR_ENCLOSURE = 'Outdoor'
INDOOR_ENCLOSURE = 'Indoor'
JANUARY_15 = date( 2026, 1, 15 )
JUNE_15 = date( 2026, 6, 15 )
OCTOBER_17 = date( 2026, 10, 17 )
OCTOBER_31 = date( 2026, 10, 31 )


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


JANUARY_LION = _animal(
   species=AFRICAN_LION,
   exhibit=AFRICA_SAVANNA,
   likelihood=100 )
JANUARY_HYENA = _animal(
   species=SPOTTED_HYENA,
   exhibit=AFRICA_SAVANNA,
   likelihood=30 )
JUNE_LION = _animal(
   species=AFRICAN_LION,
   exhibit=AFRICA_SAVANNA,
   likelihood=100 )
JUNE_HYENA = _animal(
   species=SPOTTED_HYENA,
   exhibit=AFRICA_SAVANNA,
   likelihood=80 )
OCTOBER_17_LION = _animal(
   species=AFRICAN_LION,
   exhibit=AFRICA_SAVANNA,
   likelihood=100 )
OCTOBER_31_LION = _animal(
   species=AFRICAN_LION,
   exhibit=AFRICA_SAVANNA,
   likelihood=100 )
OCTOBER_31_CAPYBARA = _animal(
   species=CAPYBARA,
   exhibit=AMERICAS,
   likelihood=90 )


def _viewable_animals_by_date() -> dict[ date, list[ Animal ] ]:
   return {
      JANUARY_15: [ JANUARY_LION, JANUARY_HYENA ],
      JUNE_15: [ JUNE_LION, JUNE_HYENA ],
      OCTOBER_17: [ OCTOBER_17_LION ],
      OCTOBER_31: [ OCTOBER_31_LION, OCTOBER_31_CAPYBARA ],
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
   existing_lion = _animal_diff(
      species=JANUARY_LION.species,
      exhibit=JANUARY_LION.exhibit,
      new_likelihood=JANUARY_LION.likelihood )
   saved_lion = ItineraryAnimalRecord(
      species=JANUARY_LION.species,
      exhibit=JANUARY_LION.exhibit,
      old_likelihood=None,
      new_likelihood=JANUARY_LION.likelihood )
   selected_exhibits = [ AFRICA_SAVANNA ]
   visit_date_temp = 28

   animals = SelectedExhibitDateChangeAnimalsBuilder.apply_on_date_change(
      AnimalCoordinator,
      existing_animals=[ existing_lion ],
      selected_exhibits=selected_exhibits,
      previously_selected_exhibits=selected_exhibits,
      saved_animal_rows=[ saved_lion ],
      visit_date=JUNE_15,
      old_visit_date=JANUARY_15,
      visit_date_temp=visit_date_temp )

   added_animals = [
      animal
      for animal in animals
      if animal.is_added
   ]
   lion = next(
      animal
      for animal in animals
      if animal.species == existing_lion.species )
   hyena = next(
      animal
      for animal in added_animals
      if animal.species == JANUARY_HYENA.species )

   assert added_animals
   assert all(
      ( animal.new_likelihood or 0 ) >= Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD
      for animal in added_animals )
   assert hyena.old_likelihood == JANUARY_HYENA.likelihood
   assert hyena.new_likelihood == JUNE_HYENA.likelihood
   assert hyena.old_likelihood < hyena.new_likelihood
   assert lion.is_added is False


def Test_ApplyOnDateChange_TestNewlySelectedExhibit_ExpectNoAddedFlag(
      stub_selected_exhibit_animal_coordinator: None ) -> None:
   existing_lion = _animal_diff(
      species=OCTOBER_17_LION.species,
      exhibit=OCTOBER_17_LION.exhibit,
      new_likelihood=OCTOBER_17_LION.likelihood )
   saved_lion = ItineraryAnimalRecord(
      species=OCTOBER_17_LION.species,
      exhibit=OCTOBER_17_LION.exhibit,
      old_likelihood=None,
      new_likelihood=OCTOBER_17_LION.likelihood )
   selected_exhibits = [ AFRICA_SAVANNA, AMERICAS ]
   previously_selected_exhibits = [ AFRICA_SAVANNA ]
   visit_date_temp = 5

   animals = SelectedExhibitDateChangeAnimalsBuilder.apply_on_date_change(
      AnimalCoordinator,
      existing_animals=[ existing_lion ],
      selected_exhibits=selected_exhibits,
      previously_selected_exhibits=previously_selected_exhibits,
      saved_animal_rows=[ saved_lion ],
      visit_date=OCTOBER_31,
      old_visit_date=OCTOBER_17,
      visit_date_temp=visit_date_temp )

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
   lion = _animal_diff(
      species=OCTOBER_31_LION.species,
      exhibit=OCTOBER_31_LION.exhibit,
      new_likelihood=OCTOBER_31_LION.likelihood )
   rhino = _animal_diff(
      species=SOUTHERN_WHITE_RHINOCEROS,
      exhibit=AFRICA_SAVANNA,
      new_likelihood=OCTOBER_31_LION.likelihood )
   hippo = _animal_diff(
      species=RIVER_HIPPOPOTAMUS,
      exhibit=AFRICA_SAVANNA,
      new_likelihood=OCTOBER_31_LION.likelihood )
   saved_lion = ItineraryAnimalRecord(
      species=lion.species,
      exhibit=lion.exhibit,
      old_likelihood=None,
      new_likelihood=lion.new_likelihood )
   selected_exhibits = [ AFRICA_SAVANNA ]
   visit_date_temp = 18

   animals = SelectedExhibitDateChangeAnimalsBuilder.apply_on_date_change(
      AnimalCoordinator,
      existing_animals=[ lion, rhino, hippo ],
      selected_exhibits=selected_exhibits,
      previously_selected_exhibits=selected_exhibits,
      saved_animal_rows=[ saved_lion ],
      visit_date=OCTOBER_17,
      old_visit_date=OCTOBER_31,
      visit_date_temp=visit_date_temp )

   by_species = { animal.species: animal for animal in animals }

   assert by_species[ rhino.species ].is_added is True
   assert by_species[ hippo.species ].is_added is True
   assert by_species[ lion.species ].is_added is False


def Test_ApplyOnDateChange_TestDeselectedExhibit_ExpectAmericasAnimalsOmitted(
      stub_selected_exhibit_animal_coordinator: None ) -> None:
   existing_lion = _animal_diff(
      species=OCTOBER_17_LION.species,
      exhibit=OCTOBER_17_LION.exhibit,
      new_likelihood=OCTOBER_17_LION.likelihood )
   saved_lion = ItineraryAnimalRecord(
      species=OCTOBER_17_LION.species,
      exhibit=OCTOBER_17_LION.exhibit,
      old_likelihood=None,
      new_likelihood=OCTOBER_17_LION.likelihood )
   saved_capybara = ItineraryAnimalRecord(
      species=OCTOBER_31_CAPYBARA.species,
      exhibit=OCTOBER_31_CAPYBARA.exhibit,
      old_likelihood=None,
      new_likelihood=OCTOBER_31_CAPYBARA.likelihood )
   selected_exhibits = [ AFRICA_SAVANNA ]
   previously_selected_exhibits = [ AFRICA_SAVANNA, AMERICAS ]
   visit_date_temp = 18

   animals = SelectedExhibitDateChangeAnimalsBuilder.apply_on_date_change(
      AnimalCoordinator,
      existing_animals=[ existing_lion ],
      selected_exhibits=selected_exhibits,
      previously_selected_exhibits=previously_selected_exhibits,
      saved_animal_rows=[ saved_lion, saved_capybara ],
      visit_date=OCTOBER_17,
      old_visit_date=OCTOBER_31,
      visit_date_temp=visit_date_temp )

   assert all(
      animal.exhibit != AMERICAS
      for animal in animals )


def Test_ApplyOnDateChange_TestSavedSpeciesExhibitMatch_ExpectSkippedDuplicate(
      stub_selected_exhibit_animal_coordinator: None ) -> None:
   outdoor_penguin = _animal_diff(
      species=AFRICAN_PENGUIN,
      exhibit=AFRICA_SAVANNA,
      enclosure_name=OUTDOOR_ENCLOSURE,
      new_likelihood=OCTOBER_17_LION.likelihood )
   indoor_penguin = _animal_diff(
      species=AFRICAN_PENGUIN,
      exhibit=AFRICA_SAVANNA,
      enclosure_name=INDOOR_ENCLOSURE,
      new_likelihood=OCTOBER_17_LION.likelihood )
   saved_outdoor = ItineraryAnimalRecord(
      species=outdoor_penguin.species,
      exhibit=outdoor_penguin.exhibit,
      enclosure_name=outdoor_penguin.enclosure_name,
      old_likelihood=None,
      new_likelihood=outdoor_penguin.new_likelihood )
   selected_exhibits = [ AFRICA_SAVANNA ]
   previously_selected_exhibits = [ AFRICA_SAVANNA, AMERICAS ]
   visit_date_temp = 18

   animals = SelectedExhibitDateChangeAnimalsBuilder.apply_on_date_change(
      AnimalCoordinator,
      existing_animals=[ outdoor_penguin, indoor_penguin ],
      selected_exhibits=selected_exhibits,
      previously_selected_exhibits=previously_selected_exhibits,
      saved_animal_rows=[ saved_outdoor ],
      visit_date=OCTOBER_17,
      old_visit_date=OCTOBER_31,
      visit_date_temp=visit_date_temp )

   indoor = next(
      animal
      for animal in animals
      if animal.enclosure_name == indoor_penguin.enclosure_name )

   assert indoor.is_added is False


def Test_ApplyOnDateChange_TestDeselectedExhibitAnimal_ExpectNotMarkedAdded(
      stub_selected_exhibit_animal_coordinator: None ) -> None:
   existing_capybara = _animal_diff(
      species=OCTOBER_31_CAPYBARA.species,
      exhibit=OCTOBER_31_CAPYBARA.exhibit,
      new_likelihood=OCTOBER_31_CAPYBARA.likelihood )
   selected_exhibits = [ AFRICA_SAVANNA ]
   previously_selected_exhibits = [ AFRICA_SAVANNA, AMERICAS ]
   visit_date_temp = 18

   animals = SelectedExhibitDateChangeAnimalsBuilder.apply_on_date_change(
      AnimalCoordinator,
      existing_animals=[ existing_capybara ],
      selected_exhibits=selected_exhibits,
      previously_selected_exhibits=previously_selected_exhibits,
      saved_animal_rows=[],
      visit_date=OCTOBER_17,
      old_visit_date=OCTOBER_31,
      visit_date_temp=visit_date_temp )

   assert animals[ Position.FIRST ].is_added is False
