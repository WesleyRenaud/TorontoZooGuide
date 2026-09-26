from __future__ import annotations

from datetime import date

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.itinerary.data_access.itinerary_animal_input import ItineraryAnimalInput
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.validation.itinerary_animal_validator import ItineraryAnimalValidator
from api.models.animal import Animal
from api.shared.calendar_dates import DateValues
from api.shared.constants import Constants
from api.shared.enums.position import Position


VISIT_DATE = date( 2026, 6, 15 )
COLD_VISIT_DATE = date( 2026, 1, 15 )
HABITAT_SWAP_DATE = date( 2026, 10, 17 )
HABITAT_SWAP_OLD_DATE = date( 2026, 10, 31 )
ALDABRA_VISIT_DATE = date( 2026, 7, 20 )
ALDABRA_OLD_DATE = date( 2026, 7, 19 )
AFRICAN_RAINFOREST_PAVILION = 'African Rainforest Pavilion'
ALDABRA_INDOOR_ENCLOSURE = 'Ring-Tailed Lemur Enclosure'
AFRICA_SAVANNA = 'Africa Savanna'
AFRICAN_LION = 'African Lion'
AFRICAN_PENGUIN = 'African Penguin'
SPOTTED_HYENA = 'Spotted Hyena'
MASAI_GIRAFFE = 'Masai Giraffe'
ALDABRA_TORTOISE = 'Aldabra Tortoise'
OUTDOOR_ENCLOSURE = 'Outdoor'
GIRAFFE_HOUSE = 'Giraffe House'
ARRIVAL_TIME = '09:30'
DEPARTURE_TIME = '17:00'
ANIMAL_DURATION_MINUTES = 8


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


UNAVAILABLE_PENGUIN = _animal(
   species=AFRICAN_PENGUIN,
   exhibit=AFRICA_SAVANNA,
   enclosure_name=OUTDOOR_ENCLOSURE,
   likelihood=100 )
COLD_HYENA = _animal(
   species=SPOTTED_HYENA,
   exhibit=AFRICA_SAVANNA,
   likelihood=10 )
COLD_GIRAFFE = _animal(
   species=MASAI_GIRAFFE,
   exhibit=AFRICA_SAVANNA,
   enclosure_name=GIRAFFE_HOUSE,
   likelihood=100 )
COLD_LION = _animal(
   species=AFRICAN_LION,
   exhibit=AFRICA_SAVANNA,
   likelihood=100 )
GIRAFFE_OUTDOOR = _animal(
   species=MASAI_GIRAFFE,
   exhibit=AFRICA_SAVANNA,
   enclosure_name=OUTDOOR_ENCLOSURE,
   likelihood=100 )
ALDABRA_OUTDOOR = _animal(
   species=ALDABRA_TORTOISE,
   exhibit=AFRICAN_RAINFOREST_PAVILION,
   enclosure_name=OUTDOOR_ENCLOSURE,
   likelihood=100 )
ALDABRA_INDOOR = _animal(
   species=ALDABRA_TORTOISE,
   exhibit=AFRICAN_RAINFOREST_PAVILION,
   enclosure_name=ALDABRA_INDOOR_ENCLOSURE,
   likelihood=100 )


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

      return animals_by_species.get( saved_animals[ Position.FIRST ].species, [] )

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
         AFRICAN_LION: [],
         UNAVAILABLE_PENGUIN.species: [ UNAVAILABLE_PENGUIN ],
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
         COLD_HYENA.species: [ COLD_HYENA ],
         COLD_GIRAFFE.species: [ COLD_GIRAFFE ],
         COLD_LION.species: [ COLD_LION ],
      } )


@pytest.fixture
def stub_giraffe_animal_coordinator(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _stub_saved_animals_lookup(
      monkeypatch,
      {
         COLD_GIRAFFE.species: [ COLD_GIRAFFE ],
      } )


@pytest.fixture
def stub_giraffe_habitat_swap_coordinator(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   outdoor_temp = 18

   def get_animals_for_saved_itinerary(
         *,
         day: int,
         month: int | str,
         year: int,
         temp: float | None,
         saved_animals: list[ ItineraryAnimalRecord ] ) -> list[ Animal ]:
      if not saved_animals:
         return []

      enclosure_name = saved_animals[ Position.FIRST ].enclosure_name

      if enclosure_name == COLD_GIRAFFE.enclosure_name and temp == outdoor_temp:
         return []

      if enclosure_name == COLD_GIRAFFE.enclosure_name:
         return [ COLD_GIRAFFE ]

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

      return [ GIRAFFE_OUTDOOR ]

   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_for_saved_itinerary',
      get_animals_for_saved_itinerary )
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_viewable_on_day',
      get_animals_viewable_on_day )


@pytest.fixture
def stub_aldabra_habitat_swap_coordinator(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   indoor_temp = 10

   def get_animals_for_saved_itinerary(
         *,
         day: int,
         month: int | str,
         year: int,
         temp: float | None,
         saved_animals: list[ ItineraryAnimalRecord ] ) -> list[ Animal ]:
      if not saved_animals:
         return []

      enclosure_name = saved_animals[ Position.FIRST ].enclosure_name

      if enclosure_name == ALDABRA_OUTDOOR.enclosure_name and temp == indoor_temp:
         return []

      if enclosure_name == ALDABRA_OUTDOOR.enclosure_name:
         return [ ALDABRA_OUTDOOR ]

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

      return [ ALDABRA_INDOOR ]

   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_for_saved_itinerary',
      get_animals_for_saved_itinerary )
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_viewable_on_day',
      get_animals_viewable_on_day )


def Test_Validate_TestUnavailableAnimal_ExpectNone(
      stub_unavailable_lion_animal_coordinator: None ) -> None:
   lion_input = ItineraryAnimalInput(
      species=AFRICAN_LION,
      exhibit=AFRICA_SAVANNA )
   penguin_input = ItineraryAnimalInput(
      species=UNAVAILABLE_PENGUIN.species,
      exhibit=UNAVAILABLE_PENGUIN.exhibit,
      enclosure_name=UNAVAILABLE_PENGUIN.enclosure_name )
   visit_date_temp = 22

   result = ItineraryAnimalValidator.validate(
      AnimalCoordinator,
      animals=[ lion_input, penguin_input ],
      new_visit_date=VISIT_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      new_visit_date_temp=visit_date_temp,
      old_visit_date=VISIT_DATE.isoformat() )

   lion_diff = next(
      diff
      for diff in result
      if diff.species == lion_input.species )
   penguin_diff = next(
      diff
      for diff in result
      if diff.species == penguin_input.species )

   assert lion_diff.new_likelihood is None
   assert penguin_diff.new_likelihood == UNAVAILABLE_PENGUIN.likelihood


def Test_ValidateOnDateChange_TestColdWeatherLikelihoods_ExpectThresholdSplit(
      stub_cold_weather_animal_coordinator: None ) -> None:
   hyena_input = ItineraryAnimalInput(
      species=COLD_HYENA.species,
      exhibit=COLD_HYENA.exhibit )
   giraffe_input = ItineraryAnimalInput(
      species=COLD_GIRAFFE.species,
      exhibit=COLD_GIRAFFE.exhibit,
      enclosure_name=COLD_GIRAFFE.enclosure_name )
   lion_input = ItineraryAnimalInput(
      species=COLD_LION.species,
      exhibit=COLD_LION.exhibit )
   visit_date_temp = -10

   result = ItineraryAnimalValidator.validate(
      AnimalCoordinator,
      animals=[ hyena_input, giraffe_input, lion_input ],
      new_visit_date=COLD_VISIT_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      new_visit_date_temp=visit_date_temp,
      old_visit_date=VISIT_DATE.isoformat(),
      visit_date_is_changing=True )

   by_species = { diff.species: diff for diff in result }

   assert by_species[ hyena_input.species ].new_likelihood == COLD_HYENA.likelihood
   assert by_species[ hyena_input.species ].new_likelihood < Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD
   assert by_species[ giraffe_input.species ].new_likelihood == COLD_GIRAFFE.likelihood
   assert by_species[ giraffe_input.species ].new_likelihood >= Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD
   assert by_species[ lion_input.species ].new_likelihood == COLD_LION.likelihood
   assert by_species[ lion_input.species ].new_likelihood >= Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD


def Test_Validate_TestSavedViewingSpot_ExpectResolvedLikelihood(
      stub_giraffe_animal_coordinator: None ) -> None:
   giraffe_input = ItineraryAnimalInput(
      species=COLD_GIRAFFE.species,
      exhibit=COLD_GIRAFFE.exhibit,
      enclosure_name=COLD_GIRAFFE.enclosure_name )
   saved_giraffe = ItineraryAnimalRecord(
      species=COLD_GIRAFFE.species,
      exhibit=COLD_GIRAFFE.exhibit,
      enclosure_name=COLD_GIRAFFE.enclosure_name,
      old_likelihood=None,
      new_likelihood=COLD_GIRAFFE.likelihood )
   visit_date_temp = -5

   result = ItineraryAnimalValidator.validate(
      AnimalCoordinator,
      animals=[ giraffe_input ],
      new_visit_date=COLD_VISIT_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      new_visit_date_temp=visit_date_temp,
      old_visit_date=COLD_VISIT_DATE.isoformat(),
      saved_animal_rows=[ saved_giraffe ] )

   assert [
      ( diff.species, diff.new_likelihood )
      for diff in result
   ] == [ ( giraffe_input.species, COLD_GIRAFFE.likelihood ) ]


def Test_ValidateOnDateChange_TestUnavailableHabitat_ExpectPreferredOutdoorSwap(
      stub_giraffe_habitat_swap_coordinator: None ) -> None:
   giraffe_input = ItineraryAnimalInput(
      species=COLD_GIRAFFE.species,
      exhibit=COLD_GIRAFFE.exhibit,
      enclosure_name=COLD_GIRAFFE.enclosure_name )
   saved_giraffe = ItineraryAnimalRecord(
      species=COLD_GIRAFFE.species,
      exhibit=COLD_GIRAFFE.exhibit,
      enclosure_name=COLD_GIRAFFE.enclosure_name,
      old_likelihood=None,
      new_likelihood=COLD_GIRAFFE.likelihood )
   visit_date_temp = 18

   result = ItineraryAnimalValidator.validate(
      AnimalCoordinator,
      animals=[ giraffe_input ],
      new_visit_date=HABITAT_SWAP_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      new_visit_date_temp=visit_date_temp,
      old_visit_date=HABITAT_SWAP_OLD_DATE.isoformat(),
      saved_animal_rows=[ saved_giraffe ],
      visit_date_is_changing=True )

   giraffes = [
      diff
      for diff in result
      if diff.species == giraffe_input.species
   ]

   assert len( giraffes ) == 1
   assert giraffes[ Position.FIRST ].enclosure_name == GIRAFFE_OUTDOOR.enclosure_name
   assert giraffes[ Position.FIRST ].is_added is False


def Test_ValidateOnDateChange_TestColdWeatherOutdoorAldabra_ExpectIndoorSwap(
      stub_aldabra_habitat_swap_coordinator: None ) -> None:
   aldabra_input = ItineraryAnimalInput(
      species=ALDABRA_OUTDOOR.species,
      exhibit=ALDABRA_OUTDOOR.exhibit,
      enclosure_name=ALDABRA_OUTDOOR.enclosure_name )
   saved_start = '10:00 AM'
   saved_aldabra = ItineraryAnimalRecord(
      species=ALDABRA_OUTDOOR.species,
      exhibit=ALDABRA_OUTDOOR.exhibit,
      enclosure_name=ALDABRA_OUTDOOR.enclosure_name,
      old_likelihood=None,
      new_likelihood=ALDABRA_OUTDOOR.likelihood,
      start_time=saved_start,
      end_time=DateValues.add_minutes_to_time(
         saved_start,
         ANIMAL_DURATION_MINUTES ) )
   visit_date_temp = 10

   result = ItineraryAnimalValidator.validate(
      AnimalCoordinator,
      animals=[ aldabra_input ],
      new_visit_date=ALDABRA_VISIT_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      new_visit_date_temp=visit_date_temp,
      old_visit_date=ALDABRA_OLD_DATE.isoformat(),
      saved_animal_rows=[ saved_aldabra ],
      visit_date_is_changing=True )

   aldabras = [
      diff
      for diff in result
      if diff.species == aldabra_input.species
   ]

   assert len( aldabras ) == 1
   assert aldabras[ Position.FIRST ].enclosure_name == ALDABRA_INDOOR.enclosure_name
   assert aldabras[ Position.FIRST ].is_added is False
   assert aldabras[ Position.FIRST ].start_time == saved_aldabra.start_time
   assert aldabras[ Position.FIRST ].end_time == saved_aldabra.end_time


def Test_ValidateOnDateChange_TestDuplicatePreferredHabitat_ExpectSingleSwap(
      stub_aldabra_habitat_swap_coordinator: None ) -> None:
   aldabra_input = ItineraryAnimalInput(
      species=ALDABRA_OUTDOOR.species,
      exhibit=ALDABRA_OUTDOOR.exhibit,
      enclosure_name=ALDABRA_OUTDOOR.enclosure_name )
   first_start = '10:00 AM'
   second_start = '11:00 AM'
   saved_rows = [
      ItineraryAnimalRecord(
         species=ALDABRA_OUTDOOR.species,
         exhibit=ALDABRA_OUTDOOR.exhibit,
         enclosure_name=ALDABRA_OUTDOOR.enclosure_name,
         old_likelihood=None,
         new_likelihood=ALDABRA_OUTDOOR.likelihood,
         start_time=first_start,
         end_time=DateValues.add_minutes_to_time(
            first_start,
            ANIMAL_DURATION_MINUTES ) ),
      ItineraryAnimalRecord(
         species=ALDABRA_OUTDOOR.species,
         exhibit=ALDABRA_OUTDOOR.exhibit,
         enclosure_name=ALDABRA_OUTDOOR.enclosure_name,
         old_likelihood=None,
         new_likelihood=ALDABRA_OUTDOOR.likelihood,
         start_time=second_start,
         end_time=DateValues.add_minutes_to_time(
            second_start,
            ANIMAL_DURATION_MINUTES ) ),
   ]
   visit_date_temp = 10

   result = ItineraryAnimalValidator.validate(
      AnimalCoordinator,
      animals=[ aldabra_input, aldabra_input ],
      new_visit_date=ALDABRA_VISIT_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      new_visit_date_temp=visit_date_temp,
      old_visit_date=ALDABRA_OLD_DATE.isoformat(),
      saved_animal_rows=saved_rows,
      visit_date_is_changing=True )

   indoor = [
      diff
      for diff in result
      if diff.enclosure_name == ALDABRA_INDOOR.enclosure_name
   ]

   assert len( indoor ) == 1
