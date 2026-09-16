from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_viewing_alert_exhibit_name_provider import AnimalViewingAlertExhibitNameProvider


TODAY = '2026-09-16'
LION = 'African Lion'
TIGER = 'Amur Tiger'
GIRAFFE = 'Giraffe'
SAVANNA = 'Africa Savanna'
EURASIA = 'Eurasia Wilds'

ANIMAL_VIEWING_ALERT_SCHEMA = """
CREATE TABLE AnimalViewingAlert (
   SPECIES              TEXT NOT NULL,
   EXHIBIT              TEXT NOT NULL,
   ALERT_MESSAGE        TEXT,
   ALERT_START_DATE     TEXT,
   ALERT_END_DATE       TEXT,
   PRIMARY KEY ( SPECIES, EXHIBIT )
);
"""


@pytest.fixture
def viewing_alert_exhibit_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ANIMAL_VIEWING_ALERT_SCHEMA )

   yield conn

   conn.close()


def _insert_alert(
      conn: sqlite3.Connection,
      *,
      species: str,
      exhibit: str,
      start_date: str | None,
      end_date: str | None ) -> None:
   conn.execute(
      """   INSERT INTO AnimalViewingAlert (
               SPECIES,
               EXHIBIT,
               ALERT_MESSAGE,
               ALERT_START_DATE,
               ALERT_END_DATE
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      (
         species,
         exhibit,
         'May be difficult to spot.',
         start_date,
         end_date,
      ) )
   conn.commit()


def Test_FetchViewingAlertExhibitNames_TestEmpty_ExpectEmptyList(
      viewing_alert_exhibit_conn: sqlite3.Connection ) -> None:
   assert AnimalViewingAlertExhibitNameProvider.fetch_viewing_alert_exhibit_names(
      viewing_alert_exhibit_conn,
      TODAY ) == []


def Test_FetchViewingAlertExhibitNames_TestCurrentAndFuture_ExpectDistinctSortedExhibits(
      viewing_alert_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_alert(
      viewing_alert_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      start_date='2026-09-01',
      end_date='2026-09-30' )
   _insert_alert(
      viewing_alert_exhibit_conn,
      species=TIGER,
      exhibit=EURASIA,
      start_date='2026-10-01',
      end_date='2026-10-15' )
   _insert_alert(
      viewing_alert_exhibit_conn,
      species=GIRAFFE,
      exhibit=SAVANNA,
      start_date='2026-09-01',
      end_date=None )

   assert AnimalViewingAlertExhibitNameProvider.fetch_viewing_alert_exhibit_names(
      viewing_alert_exhibit_conn,
      TODAY ) == [ SAVANNA, EURASIA ]


def Test_FetchViewingAlertExhibitNames_TestExpired_ExpectExcluded(
      viewing_alert_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_alert(
      viewing_alert_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      start_date='2026-08-01',
      end_date='2026-09-15' )

   assert AnimalViewingAlertExhibitNameProvider.fetch_viewing_alert_exhibit_names(
      viewing_alert_exhibit_conn,
      TODAY ) == []


def Test_FetchViewingAlertExhibitNames_TestEndingToday_ExpectIncluded(
      viewing_alert_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_alert(
      viewing_alert_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      start_date='2026-09-01',
      end_date=TODAY )

   assert AnimalViewingAlertExhibitNameProvider.fetch_viewing_alert_exhibit_names(
      viewing_alert_exhibit_conn,
      TODAY ) == [ SAVANNA ]
