from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_time_provider import ItineraryTimeProvider


TIME_PROVIDER_SCHEMA = """
CREATE TABLE ItineraryDate (
   ITINERARY_DATE       TEXT,
   ARRIVAL_TIME         TEXT,
   DEPARTURE_TIME       TEXT
);
"""

ITINERARY_DATE = '2026-06-15'
SEEDED_ARRIVAL_TIME = '9:30 AM'
SEEDED_DEPARTURE_TIME = '5:00 PM'


@pytest.fixture
def time_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( TIME_PROVIDER_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryDate (
               ITINERARY_DATE,
               ARRIVAL_TIME,
               DEPARTURE_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( ITINERARY_DATE, SEEDED_ARRIVAL_TIME, SEEDED_DEPARTURE_TIME ) )
   conn.commit()

   yield conn

   conn.close()


def _fetch_times( conn: sqlite3.Connection ) -> tuple[ str | None, str | None ]:
   row = conn.execute(
      """   SELECT ARRIVAL_TIME, DEPARTURE_TIME
            FROM ItineraryDate
            LIMIT 1;
      """
   ).fetchone()

   assert row is not None
   return row[ 'ARRIVAL_TIME' ], row[ 'DEPARTURE_TIME' ]


def Test_SetItineraryArrivalTime_TestNewTime_ExpectUpdatedArrivalOnly(
      time_provider_conn: sqlite3.Connection ) -> None:
   arrival_time = '10:15 AM'

   updated = ItineraryTimeProvider.set_itinerary_arrival_time(
      time_provider_conn,
      arrival_time )
   persisted_arrival_time, persisted_departure_time = _fetch_times(
      time_provider_conn )

   assert updated
   assert persisted_arrival_time == arrival_time
   assert persisted_departure_time == SEEDED_DEPARTURE_TIME


def Test_SetItineraryDepartureTime_TestNewTime_ExpectUpdatedDepartureOnly(
      time_provider_conn: sqlite3.Connection ) -> None:
   departure_time = '4:15 PM'

   updated = ItineraryTimeProvider.set_itinerary_departure_time(
      time_provider_conn,
      departure_time )
   persisted_arrival_time, persisted_departure_time = _fetch_times(
      time_provider_conn )

   assert updated
   assert persisted_arrival_time == SEEDED_ARRIVAL_TIME
   assert persisted_departure_time == departure_time


def Test_SetItineraryArrivalTime_TestNull_ExpectClearedArrivalOnly(
      time_provider_conn: sqlite3.Connection ) -> None:
   arrival_time = None

   updated = ItineraryTimeProvider.set_itinerary_arrival_time(
      time_provider_conn,
      arrival_time )
   persisted_arrival_time, persisted_departure_time = _fetch_times(
      time_provider_conn )

   assert updated
   assert persisted_arrival_time is None
   assert persisted_departure_time == SEEDED_DEPARTURE_TIME
