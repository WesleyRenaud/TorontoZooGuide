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
from api.models.guardians_talk import GuardiansTalk
from api.shared.calendar_dates import DateValues
from api.shared.duration_values import DurationValues
from api.shared.enums.position import Position
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


AFRICA_SAVANNA = 'Africa Savanna'
TUNDRA_TREK = 'Tundra Trek'
AFRICAN_LION = 'African Lion'
CHEETAH = 'Cheetah'
CARIBOU = 'Caribou'
ANIMAL_LIKELIHOOD = 100
ANIMAL_DURATION_MINUTES = 8
TALK_DURATION_MINUTES = 30
SAVED_VISIT_DATE = date( 2026, 6, 20 )
NEXT_VISIT_DATE = date( 2026, 6, 22 )
CARIBOU_VISIT_DATE = date( 2026, 6, 21 )

LION_INPUT = ItineraryAnimalInput(
   species=AFRICAN_LION,
   exhibit=AFRICA_SAVANNA,
)

LION_ANIMAL = Animal(
   species=AFRICAN_LION,
   exhibit=AFRICA_SAVANNA,
   likelihood=ANIMAL_LIKELIHOOD,
)

CHEETAH_INPUT = ItineraryAnimalInput(
   species=CHEETAH,
   exhibit=AFRICA_SAVANNA,
)

CHEETAH_ANIMAL = Animal(
   species=CHEETAH,
   exhibit=AFRICA_SAVANNA,
   likelihood=ANIMAL_LIKELIHOOD,
)

CARIBOU_INPUT = ItineraryAnimalInput(
   species=CARIBOU,
   exhibit=TUNDRA_TREK,
)

CARIBOU_ANIMAL = Animal(
   species=CARIBOU,
   exhibit=TUNDRA_TREK,
   likelihood=ANIMAL_LIKELIHOOD,
)

CARIBOU_TALK_LINK = GuardiansTalkAnimalRecord(
   talk_name=CARIBOU,
   location=TUNDRA_TREK,
   species=CARIBOU,
   exhibit=TUNDRA_TREK,
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
   early_arrival = '9:00 AM'
   animal_start = DateValues.add_minutes_to_time(
      early_arrival,
      ANIMAL_DURATION_MINUTES )
   saved = SavedItinerary(
      date_value=SAVED_VISIT_DATE.isoformat(),
      arrival_time=early_arrival,
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species=LION_INPUT.species,
            exhibit=LION_INPUT.exhibit,
            old_likelihood=None,
            new_likelihood=LION_ANIMAL.likelihood,
            start_time=animal_start,
            end_time=DateValues.add_minutes_to_time(
               animal_start,
               ANIMAL_DURATION_MINUTES ) ),
      ],
   )
   save_input = ItinerarySaveInput(
      date=NEXT_VISIT_DATE,
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_INPUT ],
   )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_save_validator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved )

   validated = ItinerarySaveValidator.validate_for_save(
      save_validator_conn,
      save_input,
      AnimalCoordinator,
      AttractionCoordinator,
      GuardiansCoordinator,
      WildEncounterCoordinator,
      old_visit_date=saved.date_value,
   )

   assert validated.needs_schedule_reschedule


def Test_ValidateForSave_TestDateChangeShorterDepartureCutsOffAnimal_ExpectNeedsReschedule(
      save_validator_conn: sqlite3.Connection,
      stub_save_validator_coordinators: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   animal_start = '6:30 PM'
   saved = SavedItinerary(
      date_value=SAVED_VISIT_DATE.isoformat(),
      arrival_time='9:30 AM',
      departure_time='8:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species=LION_INPUT.species,
            exhibit=LION_INPUT.exhibit,
            old_likelihood=None,
            new_likelihood=LION_ANIMAL.likelihood,
            start_time=animal_start,
            end_time=DateValues.add_minutes_to_time(
               animal_start,
               ANIMAL_DURATION_MINUTES ) ),
      ],
   )
   save_input = ItinerarySaveInput(
      date=NEXT_VISIT_DATE,
      arrival_time='09:30',
      departure_time='18:00',
      animals=[ LION_INPUT ],
   )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_save_validator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved )

   validated = ItinerarySaveValidator.validate_for_save(
      save_validator_conn,
      save_input,
      AnimalCoordinator,
      AttractionCoordinator,
      GuardiansCoordinator,
      WildEncounterCoordinator,
      old_visit_date=saved.date_value,
   )

   assert validated.needs_schedule_reschedule


def Test_ValidateForSave_TestDateChangeDeletedTalkUncoversCaribou_ExpectEnclosureDuration(
      save_validator_conn: sqlite3.Connection,
      stub_save_validator_coordinators: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   enclosure_duration_minutes = 3
   talk_start = '3:00 PM'
   saved_caribou = ItineraryAnimalRecord(
      species=CARIBOU_INPUT.species,
      exhibit=CARIBOU_INPUT.exhibit,
      old_likelihood=None,
      new_likelihood=CARIBOU_ANIMAL.likelihood,
      covered_by_talk=True,
      start_time=talk_start,
      end_time=DateValues.add_minutes_to_time(
         talk_start,
         TALK_DURATION_MINUTES ) )
   saved = SavedItinerary(
      date_value=SAVED_VISIT_DATE.isoformat(),
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[ saved_caribou ],
   )
   talk_input = ItineraryGuardiansTalkInput(
      name=CARIBOU_TALK_LINK.talk_name,
      start_time='15:00',
      end_time='15:30' )
   save_input = ItinerarySaveInput(
      date=CARIBOU_VISIT_DATE,
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ CARIBOU_INPUT ],
      guardians_talks=[ talk_input ],
   )
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
      lambda conn: saved )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ CARIBOU_TALK_LINK ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: DurationValues.minutes_to_seconds(
         enclosure_duration_minutes ) )

   validated = ItinerarySaveValidator.validate_for_save(
      save_validator_conn,
      save_input,
      AnimalCoordinator,
      AttractionCoordinator,
      GuardiansCoordinator,
      WildEncounterCoordinator,
      old_visit_date=saved.date_value,
   )

   caribou = next(
      animal
      for animal in validated.animals
      if animal.species == CARIBOU_INPUT.species )

   assert caribou.covered_by_talk is False
   assert caribou.start_time == saved_caribou.start_time
   assert caribou.end_time == DateValues.add_minutes_to_time(
      saved_caribou.start_time,
      enclosure_duration_minutes )
   assert validated.guardians_talks[ Position.FIRST ].is_deleted is True


def Test_ValidateForSave_TestDateChangeGuestAnimalTimes_ExpectCarryoverPreserved(
      save_validator_conn: sqlite3.Connection,
      stub_save_validator_coordinators: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   lion_row = ItineraryAnimalRecord(
      species=LION_INPUT.species,
      exhibit=LION_INPUT.exhibit,
      old_likelihood=None,
      new_likelihood=LION_ANIMAL.likelihood,
      start_time='9:23 AM',
      end_time='9:31 AM' )
   cheetah_row = ItineraryAnimalRecord(
      species=CHEETAH_INPUT.species,
      exhibit=CHEETAH_INPUT.exhibit,
      old_likelihood=None,
      new_likelihood=CHEETAH_ANIMAL.likelihood,
      start_time='10:30 AM',
      end_time='10:35 AM' )
   saved = SavedItinerary(
      date_value=SAVED_VISIT_DATE.isoformat(),
      arrival_time='9:15 AM',
      departure_time='5:00 PM',
      animal_rows=[ lion_row, cheetah_row ],
   )
   save_input = ItinerarySaveInput(
      date=NEXT_VISIT_DATE,
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_INPUT, CHEETAH_INPUT ],
   )
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_for_saved_itinerary',
      lambda **kwargs: {
         LION_INPUT.species: [ LION_ANIMAL ],
         CHEETAH_INPUT.species: [ CHEETAH_ANIMAL ],
      }.get( kwargs[ 'saved_animals' ][ Position.FIRST ].species, [] ) )
   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_viewable_on_day',
      lambda **kwargs: [ LION_ANIMAL, CHEETAH_ANIMAL ] )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_save_validator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved )

   validated = ItinerarySaveValidator.validate_for_save(
      save_validator_conn,
      save_input,
      AnimalCoordinator,
      AttractionCoordinator,
      GuardiansCoordinator,
      WildEncounterCoordinator,
      old_visit_date=saved.date_value,
   )

   by_species = { animal.species: animal for animal in validated.animals }

   assert by_species[ lion_row.species ].start_time == lion_row.start_time
   assert by_species[ lion_row.species ].end_time == lion_row.end_time
   assert by_species[ cheetah_row.species ].start_time == cheetah_row.start_time
   assert by_species[ cheetah_row.species ].end_time == cheetah_row.end_time
   assert validated.needs_schedule_reschedule is True


def Test_ValidateForSave_TestSameDateFixedTimeTalk_ExpectArrivalAndDepartureAdjusted(
      save_validator_conn: sqlite3.Connection,
      stub_save_validator_coordinators: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   talk_start = '10:00'
   talk_end = '10:30'
   saved = SavedItinerary(
      date_value=SAVED_VISIT_DATE.isoformat(),
      arrival_time='11:00 AM',
      departure_time='3:00 PM',
      selected_exhibits=[ AFRICA_SAVANNA ],
   )
   talk = GuardiansTalk(
      name=AFRICAN_LION,
      location=AFRICA_SAVANNA,
      x_coord=0.0,
      y_coord=0.0,
      start_time=DateValues.format_display_time_value( talk_start ),
      end_time=DateValues.format_display_time_value( talk_end ) )
   talk_input = ItineraryGuardiansTalkInput(
      name=talk.name,
      start_time=talk_start,
      end_time=talk_end )
   save_input = ItinerarySaveInput(
      date=SAVED_VISIT_DATE,
      arrival_time='11:00',
      departure_time='15:00',
      selected_exhibits=saved.selected_exhibits,
      animals=[ LION_INPUT ],
      guardians_talks=[ talk_input ],
   )
   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_save_validator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved )
   monkeypatch.setattr(
      GuardiansCoordinator,
      'get_guardians_talk_schedule',
      lambda **kwargs: [ talk ] )

   validated = ItinerarySaveValidator.validate_for_save(
      save_validator_conn,
      save_input,
      AnimalCoordinator,
      AttractionCoordinator,
      GuardiansCoordinator,
      WildEncounterCoordinator,
      old_visit_date=saved.date_value,
   )

   assert validated.arrival_time == talk_input.start_time
   assert validated.departure_time == save_input.departure_time
