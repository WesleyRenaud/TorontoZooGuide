from __future__ import annotations

import sqlite3

import pytest

from api.restrooms.data_access.restroom_alert_name_provider import RestroomAlertNameProvider


TODAY = '2026-09-16'
AFRICA = 'Africa Restaurant Restroom'
ENTRANCE = 'Entrance Restroom'
SPLASH = 'Splash Island Restroom'

RESTROOM_ALERT_SCHEMA = """
CREATE TABLE RestroomAlert (
   RESTROOM             TEXT NOT NULL PRIMARY KEY,
   ALERT_MESSAGE        TEXT,
   ALERT_START_DATE     TEXT,
   ALERT_END_DATE       TEXT
);
"""


@pytest.fixture
def restroom_alert_name_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( RESTROOM_ALERT_SCHEMA )

   yield conn

   conn.close()


def _insert_alert(
      conn: sqlite3.Connection,
      *,
      restroom: str,
      start_date: str | None,
      end_date: str | None ) -> None:
   conn.execute(
      """   INSERT INTO RestroomAlert (
               RESTROOM,
               ALERT_MESSAGE,
               ALERT_START_DATE,
               ALERT_END_DATE
            )
            VALUES ( ?, ?, ?, ? );
      """,
      (
         restroom,
         'Paper towels unavailable.',
         start_date,
         end_date,
      ) )
   conn.commit()


def Test_FetchRestroomAlertNames_TestEmpty_ExpectEmptyList(
      restroom_alert_name_conn: sqlite3.Connection ) -> None:
   assert RestroomAlertNameProvider.fetch_restroom_alert_names(
      restroom_alert_name_conn,
      TODAY ) == []


def Test_FetchRestroomAlertNames_TestCurrentAndFuture_ExpectDistinctSortedRestrooms(
      restroom_alert_name_conn: sqlite3.Connection ) -> None:
   _insert_alert(
      restroom_alert_name_conn,
      restroom=AFRICA,
      start_date='2026-09-01',
      end_date='2026-09-30' )
   _insert_alert(
      restroom_alert_name_conn,
      restroom=ENTRANCE,
      start_date='2026-10-01',
      end_date='2026-10-15' )
   _insert_alert(
      restroom_alert_name_conn,
      restroom=SPLASH,
      start_date='2026-09-01',
      end_date=None )

   assert RestroomAlertNameProvider.fetch_restroom_alert_names(
      restroom_alert_name_conn,
      TODAY ) == [ AFRICA, ENTRANCE, SPLASH ]


def Test_FetchRestroomAlertNames_TestExpired_ExpectExcluded(
      restroom_alert_name_conn: sqlite3.Connection ) -> None:
   _insert_alert(
      restroom_alert_name_conn,
      restroom=AFRICA,
      start_date='2026-08-01',
      end_date='2026-09-15' )

   assert RestroomAlertNameProvider.fetch_restroom_alert_names(
      restroom_alert_name_conn,
      TODAY ) == []


def Test_FetchRestroomAlertNames_TestEndingToday_ExpectIncluded(
      restroom_alert_name_conn: sqlite3.Connection ) -> None:
   _insert_alert(
      restroom_alert_name_conn,
      restroom=AFRICA,
      start_date='2026-09-01',
      end_date=TODAY )

   assert RestroomAlertNameProvider.fetch_restroom_alert_names(
      restroom_alert_name_conn,
      TODAY ) == [ AFRICA ]
