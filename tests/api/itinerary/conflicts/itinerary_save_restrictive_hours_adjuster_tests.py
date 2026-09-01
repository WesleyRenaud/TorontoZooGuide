from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.itinerary.conflicts.itinerary_save_restrictive_hours_adjuster import ItinerarySaveRestrictiveHoursAdjuster
from api.itinerary.data_access.itinerary_save_input import ItinerarySaveInput
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_adjustment_type import ItineraryAdjustmentType


ADJUSTER_SCHEMA = """
CREATE TABLE Itinerary (
   DATE                 TEXT        NOT NULL,
   ARRIVAL_TIME         TEXT,
   DEPARTURE_TIME       TEXT
);

CREATE TABLE ZooHours (
   OPERATING_DATE       TEXT        NOT NULL PRIMARY KEY,
   EARLY_ADMISSION_TIME TEXT,
   OPEN_TIME            TEXT        NOT NULL,
   LAST_ADMISSION_TIME  TEXT        NOT NULL,
   CLOSE_TIME           TEXT        NOT NULL
);
"""


@pytest.fixture
def adjuster_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ADJUSTER_SCHEMA )
   conn.execute(
      """   INSERT INTO Itinerary (
               DATE,
               ARRIVAL_TIME,
               DEPARTURE_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( '2026-06-20', '09:00', '17:00' ) )
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
      ( '2026-06-20', '09:00', '09:30', '18:00', '19:00' ) )
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
      ( '2026-06-22', None, '09:30', '18:00', '19:00' ) )
   conn.commit()

   yield conn

   conn.close()


def Test_Adjust_TestDateChangeFromEarlyAdmissionDay_ExpectArrivalMovedToOpen(
      adjuster_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.conflicts.itinerary_save_restrictive_hours_adjuster.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:00 AM',
         departure_time='5:00 PM',
      ) )

   save_input = ItinerarySaveInput(
      date=date( 2026, 6, 22 ),
      arrival_time='9:00 AM',
      departure_time='17:00',
   )

   updated_input, adjustments = ItinerarySaveRestrictiveHoursAdjuster.adjust(
      adjuster_conn,
      save_input,
      old_visit_date='2026-06-20',
   )

   assert updated_input.arrival_time == '09:30'
   assert len( adjustments ) == 1
   assert adjustments[ 0 ].type == ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED


def Test_Adjust_TestDateChangeWithLateDeparture_ExpectDepartureMovedToClose(
      adjuster_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.conflicts.itinerary_save_restrictive_hours_adjuster.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:30 AM',
         departure_time='8:00 PM',
      ) )

   save_input = ItinerarySaveInput(
      date=date( 2026, 6, 22 ),
      arrival_time='9:30 AM',
      departure_time='8:00 PM',
   )

   updated_input, adjustments = ItinerarySaveRestrictiveHoursAdjuster.adjust(
      adjuster_conn,
      save_input,
      old_visit_date='2026-06-20',
   )

   assert updated_input.departure_time == '19:00'
   assert len( adjustments ) == 1
   assert adjustments[ 0 ].type == ItineraryAdjustmentType.DEPARTURE_TIME_ADJUSTED
