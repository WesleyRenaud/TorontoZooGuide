from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.operations.itinerary_warning_suppressor import ItineraryWarningSuppressor
from api.shared.enums import ItineraryErrorType


STATUS_SCHEMA = """
CREATE TABLE ItineraryStatus (
   STATUS             TEXT NOT NULL PRIMARY KEY,
   IS_SUPPRESSABLE    BOOL NOT NULL
);

CREATE TABLE ItineraryStatusSuppression (
   STATUS             TEXT NOT NULL PRIMARY KEY,
   IS_SUPPRESSED      BOOL NOT NULL DEFAULT 0
);
"""


def _suppression_row(
      conn: sqlite3.Connection,
      status: str ) -> sqlite3.Row | None:
   return conn.execute(
      """   SELECT IS_SUPPRESSED
            FROM ItineraryStatusSuppression
            WHERE STATUS = ?;
      """,
      ( status, ),
   ).fetchone()


@pytest.fixture
def suppressor_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( STATUS_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryStatus (
               STATUS,
               IS_SUPPRESSABLE
            )
            VALUES ( ?, 1 );
      """,
      ( ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value, ) )
   conn.commit()

   yield conn

   conn.close()


@pytest.fixture
def empty_suppressor_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_Suppress_TestSuppressableWarning_ExpectPersisted(
      suppressor_conn: sqlite3.Connection ) -> None:
   status = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value

   result = ItineraryWarningSuppressor.suppress( suppressor_conn, status )
   row = _suppression_row( suppressor_conn, status )

   assert result.status == ItineraryErrorType.SUCCESS
   assert row is not None
   assert row[ 'IS_SUPPRESSED' ] == 1


def Test_Suppress_TestUnknownWarning_ExpectSaveFailed(
      empty_suppressor_conn: sqlite3.Connection ) -> None:
   warning = 'not-a-real-warning'

   result = ItineraryWarningSuppressor.suppress( empty_suppressor_conn, warning )

   assert result.status == ItineraryErrorType.SAVE_FAILED


def Test_Suppress_TestNonSuppressableWarning_ExpectSaveFailed(
      suppressor_conn: sqlite3.Connection ) -> None:
   status = ItineraryErrorType.SUCCESS.value

   result = ItineraryWarningSuppressor.suppress( suppressor_conn, status )

   assert result.status == ItineraryErrorType.SAVE_FAILED


def Test_Unsuppress_TestSuppressedWarning_ExpectCleared(
      suppressor_conn: sqlite3.Connection ) -> None:
   status = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value
   ItineraryWarningSuppressor.suppress( suppressor_conn, status )

   result = ItineraryWarningSuppressor.unsuppress( suppressor_conn, status )
   row = _suppression_row( suppressor_conn, status )

   assert result.status == ItineraryErrorType.SUCCESS
   assert row is None


def Test_Unsuppress_TestUnknownWarning_ExpectSaveFailed(
      empty_suppressor_conn: sqlite3.Connection ) -> None:
   warning = 'not-a-real-warning'

   result = ItineraryWarningSuppressor.unsuppress( empty_suppressor_conn, warning )

   assert result.status == ItineraryErrorType.SAVE_FAILED
