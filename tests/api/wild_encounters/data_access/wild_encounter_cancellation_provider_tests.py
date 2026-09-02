from __future__ import annotations

import sqlite3

import pytest

from api.wild_encounters.cancellations.wild_encounter_cancellation_input import WildEncounterCancellationInput
from api.wild_encounters.data_access.wild_encounter_cancellation_provider import WildEncounterCancellationProvider


KANGAROO = 'Kangaroo'
OTTER = 'Otter'
ENCOUNTER_TIME = '3:30 PM'
SECOND_ENCOUNTER_TIME = '11:00 AM'
CANCELLATION_DATE = '2026-06-15'
OTHER_DATE = '2026-06-20'

CANCELLATION_PROVIDER_SCHEMA = """
CREATE TABLE WildEncounterCancellation (
   WILD_ENCOUNTER    TEXT NOT NULL,
   CANCELLATION_DATE DATE NOT NULL,
   ENCOUNTER_TIME    TEXT NOT NULL,
   PRIMARY KEY ( WILD_ENCOUNTER, CANCELLATION_DATE, ENCOUNTER_TIME )
);
"""


@pytest.fixture
def cancellation_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( CANCELLATION_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def _cancellation_input(
      *,
      wild_encounter: str = KANGAROO,
      cancellation_date: str = CANCELLATION_DATE,
      encounter_time: str = ENCOUNTER_TIME ) -> WildEncounterCancellationInput:
   return WildEncounterCancellationInput(
      wild_encounter=wild_encounter,
      cancellation_date=cancellation_date,
      encounter_time=encounter_time )


def _insert_cancellation(
      conn: sqlite3.Connection,
      *,
      wild_encounter: str = KANGAROO,
      cancellation_date: str = CANCELLATION_DATE,
      encounter_time: str = ENCOUNTER_TIME ) -> None:
   conn.execute(
      """   INSERT INTO WildEncounterCancellation (
               WILD_ENCOUNTER, CANCELLATION_DATE, ENCOUNTER_TIME
            ) VALUES ( ?, ?, ? );
      """,
      ( wild_encounter, cancellation_date, encounter_time ),
   )


def Test_FetchCancellationRecords_TestEmpty_ExpectEmptyList(
      cancellation_provider_conn: sqlite3.Connection ) -> None:
   assert WildEncounterCancellationProvider.fetch_cancellation_records(
      cancellation_provider_conn,
      KANGAROO ) == []


def Test_FetchCancellationRecords_TestMatchingEncounter_ExpectMappedRecords(
      cancellation_provider_conn: sqlite3.Connection ) -> None:
   _insert_cancellation( cancellation_provider_conn )
   _insert_cancellation(
      cancellation_provider_conn,
      cancellation_date=OTHER_DATE,
      encounter_time=SECOND_ENCOUNTER_TIME )
   _insert_cancellation(
      cancellation_provider_conn,
      wild_encounter=OTTER )
   cancellation_provider_conn.commit()

   records = WildEncounterCancellationProvider.fetch_cancellation_records(
      cancellation_provider_conn,
      KANGAROO )

   assert [
      ( record.cancellation_date, record.encounter_time )
      for record in records
   ] == [
      ( CANCELLATION_DATE, ENCOUNTER_TIME ),
      ( OTHER_DATE, SECOND_ENCOUNTER_TIME ),
   ]


def Test_SaveCancellation_TestNewRow_ExpectTrueAndPersisted(
      cancellation_provider_conn: sqlite3.Connection ) -> None:
   assert WildEncounterCancellationProvider.save_cancellation(
      cancellation_provider_conn,
      _cancellation_input() ) is True

   records = WildEncounterCancellationProvider.fetch_cancellation_records(
      cancellation_provider_conn,
      KANGAROO )

   assert len( records ) == 1
   assert records[ 0 ].cancellation_date == CANCELLATION_DATE
   assert records[ 0 ].encounter_time == ENCOUNTER_TIME


def Test_SaveCancellation_TestDuplicate_ExpectFalse(
      cancellation_provider_conn: sqlite3.Connection ) -> None:
   WildEncounterCancellationProvider.save_cancellation(
      cancellation_provider_conn,
      _cancellation_input() )

   assert WildEncounterCancellationProvider.save_cancellation(
      cancellation_provider_conn,
      _cancellation_input() ) is False
