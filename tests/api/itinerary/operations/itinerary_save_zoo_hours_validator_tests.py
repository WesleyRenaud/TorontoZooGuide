from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.data_access.itinerary_save_input import ItinerarySaveInput
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_transportation_stations_builder import ItineraryTransportationStationsBuilder
from api.itinerary.domain.itinerary_transportations_builder import ItineraryTransportationsBuilder
from api.itinerary.operations.itinerary_save_zoo_hours_validator import ItinerarySaveZooHoursValidator
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


ZOO_HOURS_VALIDATOR_SCHEMA = """
CREATE TABLE ZooHours (
   OPERATING_DATE       TEXT        NOT NULL PRIMARY KEY,
   EARLY_ADMISSION_TIME TEXT,
   OPEN_TIME            TEXT        NOT NULL,
   LAST_ADMISSION_TIME  TEXT        NOT NULL,
   CLOSE_TIME           TEXT        NOT NULL
);
"""

VISIT_DATE = date( 2026, 6, 22 )
OPEN_TIME = '09:30'
LAST_ADMISSION_TIME = '17:00'
CLOSE_TIME = '18:00'
ITINERARY_CONTEXT = {
   'animal_coordinator': AnimalCoordinator,
   'attraction_coordinator': AttractionCoordinator,
   'guardians_coordinator': GuardiansCoordinator,
   'wild_encounter_coordinator': WildEncounterCoordinator,
   'visit_date_temp': None,
}


def _stub_saved_itinerary_transportation(
      monkeypatch: pytest.MonkeyPatch,
      saved_itinerary: SavedItinerary ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_zoo_hours_validator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved_itinerary )
   monkeypatch.setattr(
      ItineraryTransportationsBuilder,
      'build',
      lambda saved_transportations, target_date: [] )
   monkeypatch.setattr(
      ItineraryTransportationStationsBuilder,
      'attach_to_transportations',
      lambda transportations: [] )


@pytest.fixture
def zoo_hours_validator_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ZOO_HOURS_VALIDATOR_SCHEMA )
   conn.execute(
      """   INSERT INTO ZooHours (
               OPERATING_DATE,
               EARLY_ADMISSION_TIME,
               OPEN_TIME,
               LAST_ADMISSION_TIME,
               CLOSE_TIME
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      ( VISIT_DATE.isoformat(), None, OPEN_TIME, LAST_ADMISSION_TIME, CLOSE_TIME ) )
   conn.commit()

   yield conn

   conn.close()


def Test_Validate_TestDepartureAfterClose_ExpectOutOfBounds(
      zoo_hours_validator_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-20',
      arrival_time='9:30 AM',
      departure_time='6:30 PM',
   )
   save_input = ItinerarySaveInput(
      date=VISIT_DATE,
      arrival_time=OPEN_TIME,
      departure_time='19:00',
   )
   _stub_saved_itinerary_transportation( monkeypatch, saved_itinerary )

   result = ItinerarySaveZooHoursValidator.validate(
      zoo_hours_validator_conn,
      save_input,
      ITINERARY_CONTEXT )

   assert result is not None
   assert result.status == ItineraryErrorType.TIME_OUT_OF_BOUNDS
   assert result.itinerary.date == saved_itinerary.date_value
   assert result.itinerary.departure_time == saved_itinerary.departure_time


def Test_Validate_TestMissingArrivalOrDeparture_ExpectNone(
      zoo_hours_validator_conn: sqlite3.Connection ) -> None:
   save_input = ItinerarySaveInput(
      date=VISIT_DATE,
      arrival_time=None,
      departure_time=LAST_ADMISSION_TIME,
   )

   result = ItinerarySaveZooHoursValidator.validate(
      zoo_hours_validator_conn,
      save_input,
      ITINERARY_CONTEXT )

   assert result is None


def Test_Validate_TestValidHours_ExpectNone(
      zoo_hours_validator_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE.isoformat(),
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )
   save_input = ItinerarySaveInput(
      date=VISIT_DATE,
      arrival_time=OPEN_TIME,
      departure_time=LAST_ADMISSION_TIME,
   )
   _stub_saved_itinerary_transportation( monkeypatch, saved_itinerary )

   result = ItinerarySaveZooHoursValidator.validate(
      zoo_hours_validator_conn,
      save_input,
      ITINERARY_CONTEXT )

   assert result is None


def Test_Validate_TestArrivalBeforeOpen_ExpectOutOfBounds(
      zoo_hours_validator_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value=VISIT_DATE.isoformat(),
      arrival_time='8:00 AM',
      departure_time='5:00 PM',
   )
   save_input = ItinerarySaveInput(
      date=VISIT_DATE,
      arrival_time='08:00',
      departure_time=LAST_ADMISSION_TIME,
   )
   _stub_saved_itinerary_transportation( monkeypatch, saved_itinerary )

   result = ItinerarySaveZooHoursValidator.validate(
      zoo_hours_validator_conn,
      save_input,
      ITINERARY_CONTEXT )

   assert result is not None
   assert result.status == ItineraryErrorType.TIME_OUT_OF_BOUNDS
