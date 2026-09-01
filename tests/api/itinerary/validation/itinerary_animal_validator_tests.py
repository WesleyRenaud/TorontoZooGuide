from __future__ import annotations

from datetime import date

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.itinerary.data_access.itinerary_animal_input import ItineraryAnimalInput
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.validation.itinerary_animal_validator import ItineraryAnimalValidator
from api.models.animal import Animal
from api.shared.constants import Constants


VISIT_DATE = date( 2026, 6, 15 )
COLD_VISIT_DATE = date( 2026, 1, 15 )


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


def _stub_saved_animals_lookup(
      monkeypatch: pytest.MonkeyPatch,
      animals_by_species: dict[ str, list[ Animal ] ] ) -> None:
   def get_animals_for_saved_itinerary(
         *,
         day: int,
         month: int | str,
         year: int,
         temp: float | None,
         saved_animals: list[ ItineraryAnimalRecord ] ) -> list[ Animal ]:
      if not saved_animals:
         return []

      return animals_by_species.get( saved_animals[ 0 ].species, [] )

   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_for_saved_itinerary',
      get_animals_for_saved_itinerary )


@pytest.fixture
def stub_unavailable_lion_animal_coordinator(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _stub_saved_animals_lookup(
      monkeypatch,
      {
         'African Lion': [],
         'African Penguin': [
            _animal(
               species='African Penguin',
               exhibit='Africa Savanna',
               enclosure_name='Outdoor',
               likelihood=100 ),
         ],
      } )
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_viewable_on_day',
      lambda **kwargs: [] )


@pytest.fixture
def stub_cold_weather_animal_coordinator(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _stub_saved_animals_lookup(
      monkeypatch,
      {
         'Spotted Hyena': [
            _animal(
               species='Spotted Hyena',
               exhibit='Africa Savanna',
               likelihood=10 ),
         ],
         'Masai Giraffe': [
            _animal(
               species='Masai Giraffe',
               exhibit='Africa Savanna',
               enclosure_name='Giraffe House',
               likelihood=100 ),
         ],
         'African Lion': [
            _animal(
               species='African Lion',
               exhibit='Africa Savanna',
               likelihood=100 ),
         ],
      } )


@pytest.fixture
def stub_giraffe_animal_coordinator(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _stub_saved_animals_lookup(
      monkeypatch,
      {
         'Masai Giraffe': [
            _animal(
               species='Masai Giraffe',
               exhibit='Africa Savanna',
               enclosure_name='Giraffe House',
               likelihood=100 ),
         ],
      } )


@pytest.fixture
def stub_giraffe_habitat_swap_coordinator(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   def get_animals_for_saved_itinerary(
         *,
         day: int,
         month: int | str,
         year: int,
         temp: float | None,
         saved_animals: list[ ItineraryAnimalRecord ] ) -> list[ Animal ]:
      if not saved_animals:
         return []

      enclosure_name = saved_animals[ 0 ].enclosure_name

      if enclosure_name == 'Giraffe House' and temp == 18:
         return []

      if enclosure_name == 'Giraffe House':
         return [
            _animal(
               species='Masai Giraffe',
               exhibit='Africa Savanna',
               enclosure_name='Giraffe House',
               likelihood=100 ),
         ]

      return []

   def get_animals_viewable_on_day(
         *,
         day: int,
         month: int | str,
         year: int,
         temp: float | None,
         include_off_display_animals: bool,
         threshold: int | None = None,
         exhibits_to_include: list[ str ] | None = None ) -> list[ Animal ]:
      if not include_off_display_animals:
         return []

      return [
         _animal(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor',
            likelihood=100 ),
      ]

   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_for_saved_itinerary',
      get_animals_for_saved_itinerary )
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_viewable_on_day',
      get_animals_viewable_on_day )


def Test_Validate_TestUnavailableAnimal_ExpectZeroLikelihood(
      stub_unavailable_lion_animal_coordinator: None ) -> None:
   result = ItineraryAnimalValidator.validate(
      AnimalCoordinator,
      animals=[
         ItineraryAnimalInput(
            species='African Lion',
            exhibit='Africa Savanna' ),
         ItineraryAnimalInput(
            species='African Penguin',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor' ),
      ],
      new_visit_date=VISIT_DATE,
      arrival_time='09:30',
      departure_time='17:00',
      new_visit_date_temp=22,
      old_visit_date='2026-06-15' )

   assert [
      ( diff.species, ( diff.new_likelihood or 0 ) > 0 )
      for diff in result
      if diff.species == 'African Lion'
   ] == [ ( 'African Lion', False ) ]
   assert [
      ( diff.species, ( diff.new_likelihood or 0 ) > 0 )
      for diff in result
      if diff.species == 'African Penguin'
   ] == [ ( 'African Penguin', True ) ]


def Test_ValidateOnDateChange_TestColdWeatherLikelihoods_ExpectThresholdSplit(
      stub_cold_weather_animal_coordinator: None ) -> None:
   result = ItineraryAnimalValidator.validate(
      AnimalCoordinator,
      animals=[
         ItineraryAnimalInput(
            species='Spotted Hyena',
            exhibit='Africa Savanna' ),
         ItineraryAnimalInput(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            enclosure_name='Giraffe House' ),
         ItineraryAnimalInput(
            species='African Lion',
            exhibit='Africa Savanna' ),
      ],
      new_visit_date=COLD_VISIT_DATE,
      arrival_time='09:30',
      departure_time='17:00',
      new_visit_date_temp=-10,
      old_visit_date='2026-06-15',
      visit_date_is_changing=True )

   by_species = { diff.species: diff for diff in result }
   assert by_species[ 'Spotted Hyena' ].new_likelihood < Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD
   assert by_species[ 'Masai Giraffe' ].new_likelihood >= Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD
   assert by_species[ 'African Lion' ].new_likelihood >= Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD


def Test_Validate_TestSavedViewingSpot_ExpectResolvedLikelihood(
      stub_giraffe_animal_coordinator: None ) -> None:
   result = ItineraryAnimalValidator.validate(
      AnimalCoordinator,
      animals=[
         ItineraryAnimalInput(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            enclosure_name='Giraffe House' ),
      ],
      new_visit_date=COLD_VISIT_DATE,
      arrival_time='09:30',
      departure_time='17:00',
      new_visit_date_temp=-5,
      old_visit_date='2026-01-15',
      saved_animal_rows=[
         ItineraryAnimalRecord(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            enclosure_name='Giraffe House',
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
   )

   assert [ ( diff.species, diff.new_likelihood ) for diff in result ] == [
      ( 'Masai Giraffe', 100 ),
   ]


def Test_ValidateOnDateChange_TestUnavailableHabitat_ExpectPreferredOutdoorSwap(
      stub_giraffe_habitat_swap_coordinator: None ) -> None:
   result = ItineraryAnimalValidator.validate(
      AnimalCoordinator,
      animals=[
         ItineraryAnimalInput(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            enclosure_name='Giraffe House' ),
      ],
      new_visit_date=date( 2026, 10, 17 ),
      arrival_time='09:30',
      departure_time='17:00',
      new_visit_date_temp=18,
      old_visit_date='2026-10-31',
      saved_animal_rows=[
         ItineraryAnimalRecord(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            enclosure_name='Giraffe House',
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
      visit_date_is_changing=True )

   giraffes = [
      diff
      for diff in result
      if diff.species == 'Masai Giraffe'
   ]

   assert len( giraffes ) == 1
   assert giraffes[ 0 ].enclosure_name == 'Outdoor'
   assert giraffes[ 0 ].is_added is False
