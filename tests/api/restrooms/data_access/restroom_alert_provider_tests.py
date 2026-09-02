from __future__ import annotations

import sqlite3

import pytest

from api.restrooms.data_access.restroom_alert_provider import RestroomAlertProvider


RESTROOM = 'Entrance Restroom'
ALERT_START_DATE = '2026-06-01'
ALERT_END_DATE = '2026-06-30'
MESSAGE = 'Paper towels unavailable.'

RESTROOM_ALERT_SCHEMA = """
CREATE TABLE RestroomAlert (
   RESTROOM             TEXT NOT NULL PRIMARY KEY,
   ALERT_MESSAGE        TEXT,
   ALERT_START_DATE     TEXT,
   ALERT_END_DATE       TEXT
);
"""


@pytest.fixture
def restroom_alert_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( RESTROOM_ALERT_SCHEMA )

   yield conn

   conn.close()


def Test_SaveAlert_TestNewAlert_ExpectPersistsRow(
      restroom_alert_conn: sqlite3.Connection ) -> None:
   assert RestroomAlertProvider.save_alert(
      restroom_alert_conn,
      restroom=RESTROOM,
      alert_start_date=ALERT_START_DATE,
      alert_end_date=ALERT_END_DATE,
      message=MESSAGE ) is True

   row = restroom_alert_conn.execute(
      """   SELECT RESTROOM, ALERT_MESSAGE, ALERT_START_DATE, ALERT_END_DATE
            FROM RestroomAlert
            WHERE RESTROOM = ?;
      """,
      ( RESTROOM, ) ).fetchone()

   assert tuple( row ) == ( RESTROOM, MESSAGE, ALERT_START_DATE, ALERT_END_DATE )


def Test_SaveAlert_TestExistingAlert_ExpectReplacesRow(
      restroom_alert_conn: sqlite3.Connection ) -> None:
   RestroomAlertProvider.save_alert(
      restroom_alert_conn,
      restroom=RESTROOM,
      alert_start_date=ALERT_START_DATE,
      alert_end_date=ALERT_END_DATE,
      message=MESSAGE )

   assert RestroomAlertProvider.save_alert(
      restroom_alert_conn,
      restroom=RESTROOM,
      alert_start_date='2026-07-01',
      alert_end_date='2026-07-15',
      message='Updated alert.' ) is True

   rows = restroom_alert_conn.execute(
      """   SELECT ALERT_MESSAGE, ALERT_START_DATE, ALERT_END_DATE
            FROM RestroomAlert
            WHERE RESTROOM = ?;
      """,
      ( RESTROOM, ) ).fetchall()

   assert len( rows ) == 1
   assert tuple( rows[ 0 ] ) == ( 'Updated alert.', '2026-07-01', '2026-07-15' )


def Test_DeleteAlert_TestExistingAlert_ExpectRemovesRow(
      restroom_alert_conn: sqlite3.Connection ) -> None:
   RestroomAlertProvider.save_alert(
      restroom_alert_conn,
      restroom=RESTROOM,
      alert_start_date=ALERT_START_DATE,
      alert_end_date=ALERT_END_DATE,
      message=MESSAGE )

   assert RestroomAlertProvider.delete_alert(
      restroom_alert_conn,
      restroom=RESTROOM ) is True

   row = restroom_alert_conn.execute(
      """   SELECT 1
            FROM RestroomAlert
            WHERE RESTROOM = ?;
      """,
      ( RESTROOM, ) ).fetchone()

   assert row is None


def Test_DeleteAlert_TestMissingAlert_ExpectFalse(
      restroom_alert_conn: sqlite3.Connection ) -> None:
   assert RestroomAlertProvider.delete_alert(
      restroom_alert_conn,
      restroom=RESTROOM ) is False
