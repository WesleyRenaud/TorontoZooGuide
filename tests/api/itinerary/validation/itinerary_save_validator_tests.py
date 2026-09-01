from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.guardians.data_access.guardians_talk_animal_record import GuardiansTalkAnimalRecord
from api.itinerary.data_access.itinerary_animal_input import ItineraryAnimalInput
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
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

CHEETAH_INPUT = ItineraryAnimalInput(
   species='Cheetah',
   exhibit='Africa Savanna',
)

CHEETAH_ANIMAL = Animal(
   species='Cheetah',
   exhibit='Africa Savanna',
   likelihood=100,
)

CARIBOU_INPUT = ItineraryAnimalInput(
   species='Caribou',
   exhibit='Tundra Trek',
)

CARIBOU_ANIMAL = Animal(
   species='Caribou',
   exhibit='Tundra Trek',
   likelihood=100,
)

CARIBOU_TALK_LINK = GuardiansTalkAnimalRecord(
   talk_name='Caribou',
   location='Tundra Trek',
   species='Caribou',
   exhibit='Tundra Trek',
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


def Test_ValidateForSave_TestDateChangeDeletedTalkUncoversCaribou_ExpectEnclosureDuration(
      save_validator_conn: sqlite3.Connection,
      stub_save_validator_coordinators: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_for_saved_itinerary',
      lambda **kwargs: [ CARIBOU_ANIMAL ] )
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_viewable_on_day',
      lambda **kwargs: [ CARIBOU_ANIMAL ] )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_save_validator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
         animal_rows=[
            ItineraryAnimalRecord(
               species='Caribou',
               exhibit='Tundra Trek',
               old_likelihood=None,
               new_likelihood=100,
               covered_by_talk=True,
               start_time='3:00 PM',
               end_time='3:30 PM',
            ),
         ],
      ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ CARIBOU_TALK_LINK ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: 3 * 60 )

   validated = ItinerarySaveValidator.validate_for_save(
      save_validator_conn,
      ItinerarySaveInput(
         date=date( 2026, 6, 21 ),
         arrival_time='09:30',
         departure_time='17:00',
         animals=[ CARIBOU_INPUT ],
         guardians_talks=[
            ItineraryGuardiansTalkInput(
               name='Caribou',
               start_time='15:00',
               end_time='15:30',
            ),
         ],
      ),
      AnimalCoordinator,
      AttractionCoordinator,
      GuardiansCoordinator,
      WildEncounterCoordinator,
      old_visit_date='2026-06-20',
   )

   caribou = next( animal for animal in validated.animals if animal.species == 'Caribou' )

   assert caribou.covered_by_talk is False
   assert caribou.start_time == '3:00 PM'
   assert caribou.end_time == '3:03 PM'
   assert validated.guardians_talks[ 0 ].is_deleted is True


def Test_ValidateForSave_TestDateChangeGuestAnimalTimes_ExpectCarryoverPreserved(
      save_validator_conn: sqlite3.Connection,
      stub_save_validator_coordinators: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_for_saved_itinerary',
      lambda **kwargs: {
         'African Lion': [ LION_ANIMAL ],
         'Cheetah': [ CHEETAH_ANIMAL ],
      }.get( kwargs[ 'saved_animals' ][ 0 ].species, [] ) )
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_viewable_on_day',
      lambda **kwargs: [ LION_ANIMAL, CHEETAH_ANIMAL ] )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_save_validator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:15 AM',
         departure_time='5:00 PM',
         animal_rows=[
            ItineraryAnimalRecord(
               species='African Lion',
               exhibit='Africa Savanna',
               old_likelihood=None,
               new_likelihood=100,
               start_time='9:23 AM',
               end_time='9:31 AM',
            ),
            ItineraryAnimalRecord(
               species='Cheetah',
               exhibit='Africa Savanna',
               old_likelihood=None,
               new_likelihood=100,
               start_time='10:30 AM',
               end_time='10:35 AM',
            ),
         ],
      ) )

   validated = ItinerarySaveValidator.validate_for_save(
      save_validator_conn,
      ItinerarySaveInput(
         date=date( 2026, 6, 22 ),
         arrival_time='09:30',
         departure_time='17:00',
         animals=[ LION_INPUT, CHEETAH_INPUT ],
      ),
      AnimalCoordinator,
      AttractionCoordinator,
      GuardiansCoordinator,
      WildEncounterCoordinator,
      old_visit_date='2026-06-20',
   )

   by_species = { animal.species: animal for animal in validated.animals }

   assert by_species[ 'African Lion' ].start_time == '9:23 AM'
   assert by_species[ 'African Lion' ].end_time == '9:31 AM'
   assert by_species[ 'Cheetah' ].start_time == '10:30 AM'
   assert by_species[ 'Cheetah' ].end_time == '10:35 AM'
   assert validated.needs_schedule_reschedule is True
