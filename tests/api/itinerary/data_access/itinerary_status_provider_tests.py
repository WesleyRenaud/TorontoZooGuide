from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.shared.enums import ItineraryErrorType
from api.shared.value_conversion import ValueConversion


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

STATUS_ROWS = [
   ( ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value, 1 ),
   ( ItineraryErrorType.ITEM_NOT_ON_ITINERARY.value, 1 ),
   ( ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS.value, 0 ),
   ( ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT.value, 0 ),
   ( ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL.value, 0 ),
   ( ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL.value, 0 ),
   ( ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS.value, 0 ),
   ( ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED.value, 0 ),
]


@pytest.fixture
def status_db() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.executescript( STATUS_SCHEMA )
   conn.executemany(
      'INSERT INTO ItineraryStatus ( STATUS, IS_SUPPRESSABLE ) VALUES ( ?, ? );',
      STATUS_ROWS )
   conn.commit()
   yield conn
   conn.close()


def Test_FetchItineraryStatuses_TestSeededRows_ExpectMappedRecords(
      status_db: sqlite3.Connection ) -> None:
   statuses = ItineraryStatusProvider.fetch_itinerary_statuses( status_db )

   suppressable_status = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE
   matching = next(
      record
      for record in statuses
      if record.status == suppressable_status.value )

   assert len( statuses ) == len( STATUS_ROWS )
   assert all( record.status for record in statuses )
   assert matching.is_suppressable is True
   assert matching.is_suppressed is False


@pytest.mark.parametrize(
   'status, expected',
   [
      (
         ItineraryErrorType( status_value ),
         ValueConversion.as_boolean( is_suppressable ),
      )
      for status_value, is_suppressable in STATUS_ROWS
   ] )
def Test_IsItineraryStatusSuppressable(
      status_db: sqlite3.Connection,
      status: ItineraryErrorType,
      expected: bool ) -> None:
   is_suppressable = ItineraryStatusProvider.is_itinerary_status_suppressable(
      status_db,
      status )

   assert is_suppressable is expected


def Test_IsItineraryStatusSuppressable_TestUnknownStatus_ExpectFalse(
      status_db: sqlite3.Connection ) -> None:
   status = ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP

   is_suppressable = ItineraryStatusProvider.is_itinerary_status_suppressable(
      status_db,
      status )

   assert is_suppressable is False


def Test_SuppressItineraryStatus_TestSuppressableType_ExpectPersisted(
      status_db: sqlite3.Connection ) -> None:
   status = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE

   ItineraryStatusProvider.suppress_itinerary_status( status_db, status )
   is_suppressed = ItineraryStatusProvider.is_itinerary_error_suppressed(
      status_db,
      status )
   suppressed_values = ItineraryStatusProvider.fetch_suppressed_status_values(
      status_db )

   assert is_suppressed
   assert suppressed_values == [ status.value ]


def Test_UnsuppressItineraryStatus_TestAfterSuppress_ExpectCleared(
      status_db: sqlite3.Connection ) -> None:
   status = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE
   ItineraryStatusProvider.suppress_itinerary_status( status_db, status )

   ItineraryStatusProvider.unsuppress_itinerary_status( status_db, status )
   is_suppressed = ItineraryStatusProvider.is_itinerary_error_suppressed(
      status_db,
      status )
   suppressed_values = ItineraryStatusProvider.fetch_suppressed_status_values(
      status_db )

   assert not is_suppressed
   assert suppressed_values == []


def Test_IsItineraryErrorSuppressed_TestNonSuppressableType_ExpectFalse(
      status_db: sqlite3.Connection ) -> None:
   status = ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS

   is_suppressed = ItineraryStatusProvider.is_itinerary_error_suppressed(
      status_db,
      status )

   assert not is_suppressed


def Test_ClearItineraryStatusSuppressions_TestAfterSuppress_ExpectCleared(
      status_db: sqlite3.Connection ) -> None:
   status = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE
   ItineraryStatusProvider.suppress_itinerary_status( status_db, status )
   cur = status_db.cursor()

   ItineraryStatusProvider.clear_itinerary_status_suppressions( cur )
   status_db.commit()
   cur.close()
   is_suppressed = ItineraryStatusProvider.is_itinerary_error_suppressed(
      status_db,
      status )

   assert not is_suppressed
