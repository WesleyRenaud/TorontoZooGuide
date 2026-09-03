from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
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

NON_SUPPRESSABLE_ERROR_TYPES = [
   ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
   ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
   ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
   ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
   ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
   ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED,
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

   assert len( statuses ) == len( STATUS_ROWS )
   assert all( record.status for record in statuses )
   assert any(
      record.status == ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value
      and record.is_suppressable
      and not record.is_suppressed
      for record in statuses )


def Test_IsItineraryStatusSuppressable_TestKnownStatuses_ExpectExpectedFlags(
      status_db: sqlite3.Connection ) -> None:
   assert ItineraryStatusProvider.is_itinerary_status_suppressable(
      status_db,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )
   assert ItineraryStatusProvider.is_itinerary_status_suppressable(
      status_db,
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY )
   assert not ItineraryStatusProvider.is_itinerary_status_suppressable(
      status_db,
      ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS )
   assert not ItineraryStatusProvider.is_itinerary_status_suppressable(
      status_db,
      ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED )

   assert not ItineraryStatusProvider.is_itinerary_status_suppressable(
      status_db,
      ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP )


def Test_SuppressItineraryStatus_TestSuppressableType_ExpectPersisted(
      status_db: sqlite3.Connection ) -> None:
   ItineraryStatusProvider.suppress_itinerary_status(
      status_db,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   assert ItineraryStatusProvider.is_itinerary_error_suppressed(
      status_db,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )
   assert ItineraryStatusProvider.fetch_suppressed_status_values( status_db ) == [
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value,
   ]


def Test_SuppressItineraryStatus_TestNonSuppressableTypes_ExpectIgnored(
      status_db: sqlite3.Connection ) -> None:
   for error_type in NON_SUPPRESSABLE_ERROR_TYPES:
      ItineraryStatusProvider.suppress_itinerary_status( status_db, error_type )

      assert not ItineraryStatusProvider.is_itinerary_error_suppressed(
         status_db,
         error_type )
      assert error_type.value not in ItineraryStatusProvider.fetch_suppressed_status_values(
         status_db )


def Test_IsItineraryErrorSuppressed_TestNonSuppressableType_ExpectFalse(
      status_db: sqlite3.Connection ) -> None:
   assert not ItineraryStatusProvider.is_itinerary_error_suppressed(
      status_db,
      ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS )


def Test_ClearItineraryStatusSuppressions_TestAfterSuppress_ExpectCleared(
      status_db: sqlite3.Connection ) -> None:
   ItineraryStatusProvider.suppress_itinerary_status(
      status_db,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   cur = status_db.cursor()
   ItineraryStatusProvider.clear_itinerary_status_suppressions( cur )
   status_db.commit()
   cur.close()

   assert not ItineraryStatusProvider.is_itinerary_error_suppressed(
      status_db,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )
