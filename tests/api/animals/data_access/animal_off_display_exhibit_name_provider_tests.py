from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_off_display_exhibit_name_provider import AnimalOffDisplayExhibitNameProvider


TODAY = '2026-09-16'
LION = 'African Lion'
TIGER = 'Amur Tiger'
GIRAFFE = 'Giraffe'
SAVANNA = 'Africa Savanna'
EURASIA = 'Eurasia Wilds'

ANIMAL_STATUS_SCHEMA = """
CREATE TABLE AnimalStatus (
   SPECIES              TEXT NOT NULL,
   EXHIBIT              TEXT NOT NULL,
   VIEWING_SCOPE        TEXT NOT NULL,
   IS_OFF_DISPLAY       INTEGER NOT NULL,
   OFF_DISPLAY_START    TEXT,
   OFF_DISPLAY_END      TEXT,
   OFF_DISPLAY_MESSAGE  TEXT,
   PRIMARY KEY ( SPECIES, EXHIBIT, VIEWING_SCOPE )
);
"""


@pytest.fixture
def off_display_exhibit_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ANIMAL_STATUS_SCHEMA )

   yield conn

   conn.close()


def _insert_status(
      conn: sqlite3.Connection,
      *,
      species: str,
      exhibit: str,
      viewing_scope: str = 'all',
      is_off_display: int = 1,
      start_date: str | None,
      end_date: str | None ) -> None:
   conn.execute(
      """   INSERT INTO AnimalStatus (
               SPECIES,
               EXHIBIT,
               VIEWING_SCOPE,
               IS_OFF_DISPLAY,
               OFF_DISPLAY_START,
               OFF_DISPLAY_END,
               OFF_DISPLAY_MESSAGE
            )
            VALUES ( ?, ?, ?, ?, ?, ?, ? );
      """,
      (
         species,
         exhibit,
         viewing_scope,
         is_off_display,
         start_date,
         end_date,
         'Off display.',
      ) )
   conn.commit()


def Test_FetchOffDisplayExhibitNames_TestEmpty_ExpectEmptyList(
      off_display_exhibit_conn: sqlite3.Connection ) -> None:
   assert AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names(
      off_display_exhibit_conn,
      TODAY ) == []


def Test_FetchOffDisplayExhibitNames_TestCurrentAndFuture_ExpectDistinctSortedExhibits(
      off_display_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_status(
      off_display_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      start_date='2026-09-01',
      end_date='2026-09-30' )
   _insert_status(
      off_display_exhibit_conn,
      species=TIGER,
      exhibit=EURASIA,
      start_date='2026-10-01',
      end_date='2026-10-15' )
   _insert_status(
      off_display_exhibit_conn,
      species=GIRAFFE,
      exhibit=SAVANNA,
      start_date='2026-09-01',
      end_date=None )

   assert AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names(
      off_display_exhibit_conn,
      TODAY ) == [ SAVANNA, EURASIA ]


def Test_FetchOffDisplayExhibitNames_TestExpiredAndOnDisplay_ExpectExcluded(
      off_display_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_status(
      off_display_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      start_date='2026-08-01',
      end_date='2026-09-15' )
   _insert_status(
      off_display_exhibit_conn,
      species=TIGER,
      exhibit=EURASIA,
      is_off_display=0,
      start_date='2026-09-01',
      end_date='2026-09-30' )

   assert AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names(
      off_display_exhibit_conn,
      TODAY ) == []


def Test_FetchOffDisplayExhibitNames_TestEndingToday_ExpectIncluded(
      off_display_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_status(
      off_display_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      start_date='2026-09-01',
      end_date=TODAY )

   assert AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names(
      off_display_exhibit_conn,
      TODAY ) == [ SAVANNA ]


def Test_FetchOffDisplayExhibitNames_TestDuplicateScopes_ExpectDistinctExhibit(
      off_display_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_status(
      off_display_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      viewing_scope='indoor',
      start_date='2026-09-01',
      end_date=None )
   _insert_status(
      off_display_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      viewing_scope='outdoor',
      start_date='2026-10-01',
      end_date='2026-10-31' )

   assert AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names(
      off_display_exhibit_conn,
      TODAY ) == [ SAVANNA ]
