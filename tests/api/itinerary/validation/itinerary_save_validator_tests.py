from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.data_access.itinerary_animal_input import ItineraryAnimalInput
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_save_input import ItinerarySaveInput
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.validation.itinerary_save_validator import ItinerarySaveValidator
from api.models.animal import Animal
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


LION_INPUT = ItineraryAnimalInput(
   species='African Lion',
   exhibit='Africa Savanna',
)

LION_ANIMAL = Animal(
   species='African Lion',
   exhibit='Africa Savanna',
   likelihood=100,
)


@pytest.fixture
def save_validator_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


@pytest.fixture
def stub_save_validator_coordinators(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GuardiansCoordinator,
      'get_guardians_talk_schedule',
      lambda **kwargs: [] )
   monkeypatch.setattr(
      WildEncounterCoordinator,
      'get_wild_encounter_schedule',
      lambda **kwargs: [] )
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_for_saved_itinerary',
      lambda **kwargs: [ LION_ANIMAL ] )
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_viewable_on_day',
      lambda **kwargs: [ LION_ANIMAL ] )
   monkeypatch.setattr(
      AttractionCoordinator,
      'get_attractions_for_saved_itinerary',
      lambda **kwargs: [] )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_save_validator.ItinerarySaveAttractionSplitBuilder.split_names',
      lambda conn, attraction_names: ( list( attraction_names ), [] ) )


def Test_ValidateForSave_TestDateChangeAdjustedArrivalCutsOffAnimal_ExpectNeedsReschedule(
      save_validator_conn: sqlite3.Connection,
      stub_save_validator_coordinators: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_save_validator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:00 AM',
         departure_time='5:00 PM',
         animal_rows=[
            ItineraryAnimalRecord(
               species='African Lion',
               exhibit='Africa Savanna',
               old_likelihood=None,
               new_likelihood=100,
               start_time='9:08 AM',
               end_time='9:16 AM',
            ),
         ],
      ) )

   validated = ItinerarySaveValidator.validate_for_save(
      save_validator_conn,
      ItinerarySaveInput(
         date=date( 2026, 6, 22 ),
         arrival_time='09:30',
         departure_time='17:00',
         animals=[ LION_INPUT ],
      ),
      AnimalCoordinator,
      AttractionCoordinator,
      GuardiansCoordinator,
      WildEncounterCoordinator,
      old_visit_date='2026-06-20',
   )

   assert validated.needs_schedule_reschedule


def Test_ValidateForSave_TestDateChangeShorterDepartureCutsOffAnimal_ExpectNeedsReschedule(
      save_validator_conn: sqlite3.Connection,
      stub_save_validator_coordinators: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_save_validator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:30 AM',
         departure_time='8:00 PM',
         animal_rows=[
            ItineraryAnimalRecord(
               species='African Lion',
               exhibit='Africa Savanna',
               old_likelihood=None,
               new_likelihood=100,
               start_time='6:30 PM',
               end_time='6:38 PM',
            ),
         ],
      ) )

   validated = ItinerarySaveValidator.validate_for_save(
      save_validator_conn,
      ItinerarySaveInput(
         date=date( 2026, 6, 22 ),
         arrival_time='09:30',
         departure_time='18:00',
         animals=[ LION_INPUT ],
      ),
      AnimalCoordinator,
      AttractionCoordinator,
      GuardiansCoordinator,
      WildEncounterCoordinator,
      old_visit_date='2026-06-20',
   )

   assert validated.needs_schedule_reschedule
