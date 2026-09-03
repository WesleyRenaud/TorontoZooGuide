from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.transportation.data_access.transportation_provider import TransportationProvider

TRANSPORTATION_PROVIDER_SCHEMA = """
CREATE TABLE Attraction (
   NAME                                  TEXT NOT NULL PRIMARY KEY,
   FREE_WITH_ADMISSION                   INTEGER NOT NULL,
   DESCRIPTION                           TEXT NOT NULL,
   INFO_LINK                             TEXT NOT NULL,
   HYPERLINK_TEXT                        TEXT NOT NULL,
   X_COORD                               REAL NOT NULL,
   Y_COORD                               REAL NOT NULL,
   DEFAULT_ITINERARY_DURATION_MINUTES    INTEGER NOT NULL,
   REGION                                TEXT NOT NULL,
   IS_ALSO_TRANSPORTATION                INTEGER NOT NULL
);

CREATE TABLE Transportation (
   NAME                 TEXT NOT NULL PRIMARY KEY,
   IS_ALSO_ATTRACTION   INTEGER NOT NULL
);

CREATE TABLE AttractionHoursSchedule (
   ATTRACTION                      TEXT NOT NULL,
   SCHEDULE_START_DATE             TEXT NOT NULL,
   SCHEDULE_END_DATE               TEXT,
   WEEKDAY_START_TIME              TEXT NOT NULL,
   WEEKDAY_END_TIME                TEXT NOT NULL,
   WEEKEND_HOLIDAY_START_TIME      TEXT NOT NULL,
   WEEKEND_HOLIDAY_END_TIME        TEXT NOT NULL,
   PRIMARY KEY ( ATTRACTION, SCHEDULE_START_DATE )
);
"""

ZOOMOBILE = 'Zoomobile'
VISIT_DATE = date( 2026, 6, 15 )

@pytest.fixture
def transportation_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( TRANSPORTATION_PROVIDER_SCHEMA )

   yield conn

   conn.close()

def _insert_zoomobile( conn: sqlite3.Connection ) -> None:
   conn.execute(
      """   INSERT INTO Attraction (
               NAME,
               FREE_WITH_ADMISSION,
               DESCRIPTION,
               INFO_LINK,
               HYPERLINK_TEXT,
               X_COORD,
               Y_COORD,
               DEFAULT_ITINERARY_DURATION_MINUTES,
               REGION,
               IS_ALSO_TRANSPORTATION
            )
            VALUES ( ?, 1, ?, ?, ?, ?, ?, ?, ?, 1 );
      """,
      (
         ZOOMOBILE,
         'Zoomobile ride',
         'https://example.com',
         'Learn more',
         1.0,
         2.0,
         60,
         'Main Entrance',
      ),
   )
   conn.execute(
      """   INSERT INTO Transportation (
               NAME,
               IS_ALSO_ATTRACTION
            )
            VALUES ( ?, 1 );
      """,
      ( ZOOMOBILE, ),
   )
   conn.execute(
      """   INSERT INTO AttractionHoursSchedule (
               ATTRACTION,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               WEEKDAY_START_TIME,
               WEEKDAY_END_TIME,
               WEEKEND_HOLIDAY_START_TIME,
               WEEKEND_HOLIDAY_END_TIME
            )
            VALUES ( ?, ?, ?, ?, ?, ?, ? );
      """,
      (
         ZOOMOBILE,
         '2026-01-01',
         '2026-12-31',
         '10:00 AM',
         '5:00 PM',
         '10:00 AM',
         '6:00 PM',
      ),
   )

def Test_FetchTransportationRecords_TestEmpty_ExpectEmptyList(
      transportation_provider_conn: sqlite3.Connection ) -> None:
   assert TransportationProvider.fetch_transportation_records(
      transportation_provider_conn,
      VISIT_DATE ) == []

def Test_FetchTransportationRecords_TestPopulated_ExpectMappedFields(
      transportation_provider_conn: sqlite3.Connection ) -> None:
   _insert_zoomobile( transportation_provider_conn )
   transportation_provider_conn.commit()

   records = TransportationProvider.fetch_transportation_records(
      transportation_provider_conn,
      VISIT_DATE )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.name == ZOOMOBILE
   assert record.is_also_attraction is True
   assert record.free_with_admission is True
   assert record.description == 'Zoomobile ride'
   assert record.weekday_start_time == '10:00 AM'
   assert record.weekend_holiday_end_time == '6:00 PM'
