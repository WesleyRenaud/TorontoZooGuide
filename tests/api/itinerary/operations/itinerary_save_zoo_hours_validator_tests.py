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

ITINERARY_CONTEXT = {
   'animal_coordinator': AnimalCoordinator,
   'attraction_coordinator': AttractionCoordinator,
   'guardians_coordinator': GuardiansCoordinator,
   'wild_encounter_coordinator': WildEncounterCoordinator,
   'visit_date_temp': None,
}


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
      ( '2026-06-22', None, '09:30', '17:00', '18:00' ) )
   conn.commit()

   yield conn

   conn.close()


def Test_Validate_TestDepartureAfterClose_ExpectOutOfBounds(
      zoo_hours_validator_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_zoo_hours_validator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:30 AM',
         departure_time='6:30 PM',
      ) )
   monkeypatch.setattr(
      ItineraryTransportationsBuilder,
      'build',
      lambda saved_transportations, target_date: [] )
   monkeypatch.setattr(
      ItineraryTransportationStationsBuilder,
      'attach_to_transportations',
      lambda transportations: [] )

   save_input = ItinerarySaveInput(
      date=date( 2026, 6, 22 ),
      arrival_time='09:30',
      departure_time='19:00',
   )

   result = ItinerarySaveZooHoursValidator.validate(
      zoo_hours_validator_conn,
      save_input,
      ITINERARY_CONTEXT )

   assert result is not None
   assert result.status == ItineraryErrorType.TIME_OUT_OF_BOUNDS
   assert result.itinerary.date == '2026-06-20'
   assert result.itinerary.departure_time == '6:30 PM'
