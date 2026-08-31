from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.seed.user_itinerary_config_cleaner import UserItineraryConfigCleaner
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
def config_cleaner_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
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


def Test_Clear_TestSuppressedWarning_ExpectCleared(
      config_cleaner_conn: sqlite3.Connection ) -> None:
   ItineraryStatusProvider.suppress_itinerary_status(
      config_cleaner_conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   cur = config_cleaner_conn.cursor()
   UserItineraryConfigCleaner.clear( cur )
   config_cleaner_conn.commit()
   cur.close()

   assert not ItineraryStatusProvider.is_itinerary_error_suppressed(
      config_cleaner_conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )
