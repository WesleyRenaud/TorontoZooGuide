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


def Test_Suppress_TestSuppressableWarning_ExpectPersisted(
      suppressor_conn: sqlite3.Connection ) -> None:
   result = ItineraryWarningSuppressor.suppress(
      suppressor_conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value )

   row = suppressor_conn.execute(
      """   SELECT IS_SUPPRESSED
            FROM ItineraryStatusSuppression
            WHERE STATUS = ?;
      """,
      ( ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value, ),
   ).fetchone()

   assert result.status == ItineraryErrorType.SUCCESS
   assert row is not None
   assert row[ 'IS_SUPPRESSED' ] == 1


def Test_Suppress_TestUnknownWarning_ExpectSaveFailed() -> None:
   conn = sqlite3.connect( ':memory:' )

   try:
      result = ItineraryWarningSuppressor.suppress( conn, 'not-a-real-warning' )

      assert result.status == ItineraryErrorType.SAVE_FAILED
   finally:
      conn.close()
