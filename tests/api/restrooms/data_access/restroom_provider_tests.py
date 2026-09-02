from __future__ import annotations

import sqlite3

import pytest

from api.restrooms.data_access.restroom_provider import RestroomProvider


RESTROOM_A = 'Entrance Restroom'
RESTROOM_B = 'Africa Restroom'

RESTROOM_PROVIDER_SCHEMA = """
CREATE TABLE Restroom (
   TITLE    TEXT  NOT NULL PRIMARY KEY,
   X_COORD  REAL  NOT NULL,
   Y_COORD  REAL  NOT NULL
);

CREATE TABLE RestroomStatus (
   RESTROOM         TEXT NOT NULL PRIMARY KEY,
   IS_CLOSED        INTEGER NOT NULL,
   CLOSED_MESSAGE   TEXT,
   CLOSED_START     TEXT,
   CLOSED_END       TEXT
);

CREATE TABLE RestroomAlert (
   RESTROOM          TEXT NOT NULL PRIMARY KEY,
   ALERT_MESSAGE     TEXT NOT NULL,
   ALERT_START_DATE  TEXT,
   ALERT_END_DATE    TEXT
);
"""


@pytest.fixture
def restroom_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( RESTROOM_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def _insert_restroom(
      conn: sqlite3.Connection,
      *,
      title: str,
      x_coord: float = 1.0,
      y_coord: float = 2.0 ) -> None:
   conn.execute(
      """   INSERT INTO Restroom ( TITLE, X_COORD, Y_COORD )
            VALUES ( ?, ?, ? );
      """,
      ( title, x_coord, y_coord ),
   )


def Test_FetchRestroomNames_TestEmpty_ExpectEmptyList(
      restroom_provider_conn: sqlite3.Connection ) -> None:
   assert RestroomProvider.fetch_restroom_names( restroom_provider_conn ) == []


def Test_FetchRestroomNames_TestPopulated_ExpectTitles(
      restroom_provider_conn: sqlite3.Connection ) -> None:
   _insert_restroom( restroom_provider_conn, title=RESTROOM_A )
   _insert_restroom( restroom_provider_conn, title=RESTROOM_B )
   restroom_provider_conn.commit()

   names = RestroomProvider.fetch_restroom_names( restroom_provider_conn )

   assert set( names ) == { RESTROOM_A, RESTROOM_B }


def Test_FetchRestroomRecords_TestEmpty_ExpectEmptyList(
      restroom_provider_conn: sqlite3.Connection ) -> None:
   assert RestroomProvider.fetch_restroom_records( restroom_provider_conn ) == []


def Test_FetchRestroomRecords_TestWithoutStatusOrAlert_ExpectNullJoinedFields(
      restroom_provider_conn: sqlite3.Connection ) -> None:
   _insert_restroom(
      restroom_provider_conn,
      title=RESTROOM_A,
      x_coord=10.5,
      y_coord=20.5 )
   restroom_provider_conn.commit()

   records = RestroomProvider.fetch_restroom_records( restroom_provider_conn )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.title == RESTROOM_A
   assert record.x_coord == 10.5
   assert record.y_coord == 20.5
   assert record.is_closed is None
   assert record.closed_message is None
   assert record.closed_start is None
   assert record.closed_end is None
   assert record.alert_message is None
   assert record.alert_start_date is None
   assert record.alert_end_date is None


def Test_FetchRestroomRecords_TestWithStatusAndAlert_ExpectJoinedFields(
      restroom_provider_conn: sqlite3.Connection ) -> None:
   _insert_restroom( restroom_provider_conn, title=RESTROOM_A )
   _insert_restroom( restroom_provider_conn, title=RESTROOM_B )
   restroom_provider_conn.execute(
      """   INSERT INTO RestroomStatus (
               RESTROOM, IS_CLOSED, CLOSED_MESSAGE, CLOSED_START, CLOSED_END
            ) VALUES ( ?, ?, ?, ?, ? );
      """,
      ( RESTROOM_A, 1, 'Out of order.', '2026-06-01', '2026-06-30' ),
   )
   restroom_provider_conn.execute(
      """   INSERT INTO RestroomAlert (
               RESTROOM, ALERT_MESSAGE, ALERT_START_DATE, ALERT_END_DATE
            ) VALUES ( ?, ?, ?, ? );
      """,
      ( RESTROOM_A, 'Limited stalls.', '2026-06-10', '2026-06-20' ),
   )
   restroom_provider_conn.commit()

   records = RestroomProvider.fetch_restroom_records( restroom_provider_conn )
   by_title = { record.title: record for record in records }

   assert set( by_title ) == { RESTROOM_A, RESTROOM_B }
   assert by_title[ RESTROOM_A ].is_closed == 1
   assert by_title[ RESTROOM_A ].closed_message == 'Out of order.'
   assert by_title[ RESTROOM_A ].closed_start == '2026-06-01'
   assert by_title[ RESTROOM_A ].closed_end == '2026-06-30'
   assert by_title[ RESTROOM_A ].alert_message == 'Limited stalls.'
   assert by_title[ RESTROOM_A ].alert_start_date == '2026-06-10'
   assert by_title[ RESTROOM_A ].alert_end_date == '2026-06-20'
   assert by_title[ RESTROOM_B ].is_closed is None
   assert by_title[ RESTROOM_B ].alert_message is None
