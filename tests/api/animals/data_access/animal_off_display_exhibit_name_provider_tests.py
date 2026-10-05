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
   OFF_DISPLAY_FOR_SEASON INTEGER NOT NULL DEFAULT 0,
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
      is_off_display_for_season: int = 0,
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
               OFF_DISPLAY_MESSAGE,
               OFF_DISPLAY_FOR_SEASON
            )
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ? );
      """,
      (
         species,
         exhibit,
         viewing_scope,
         is_off_display,
         start_date,
         end_date,
         'Off display.',
         is_off_display_for_season,
      ) )
   conn.commit()


def Test_FetchOffDisplayExhibitNames_TestEmpty_ExpectEmptyList(
      off_display_exhibit_conn: sqlite3.Connection ) -> None:
   off_display_exhibit_names = AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names(
      off_display_exhibit_conn,
      TODAY,
      for_season_only=False )

   assert off_display_exhibit_names == []


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

   off_display_exhibit_names = AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names(
      off_display_exhibit_conn,
      TODAY,
      for_season_only=False )

   assert off_display_exhibit_names == [ SAVANNA, EURASIA ]


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

   off_display_exhibit_names = AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names(
      off_display_exhibit_conn,
      TODAY,
      for_season_only=False )

   assert off_display_exhibit_names == []


def Test_FetchOffDisplayExhibitNames_TestEndingToday_ExpectIncluded(
      off_display_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_status(
      off_display_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      start_date='2026-09-01',
      end_date=TODAY )

   off_display_exhibit_names = AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names(
      off_display_exhibit_conn,
      TODAY,
      for_season_only=False )

   assert off_display_exhibit_names == [ SAVANNA ]


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

   off_display_exhibit_names = AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names(
      off_display_exhibit_conn,
      TODAY,
      for_season_only=False )

   assert off_display_exhibit_names == [ SAVANNA ]


def Test_FetchOffDisplayExhibitNamesForSpecies_TestMatchingSpecies_ExpectThoseExhibits(
      off_display_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_status(
      off_display_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      start_date='2026-09-01',
      end_date=None )
   _insert_status(
      off_display_exhibit_conn,
      species=TIGER,
      exhibit=EURASIA,
      start_date='2026-09-01',
      end_date=None )

   off_display_exhibit_names_for_species = AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names_for_species(
      off_display_exhibit_conn,
      TODAY,
      LION,
      for_season_only=False )

   assert off_display_exhibit_names_for_species == [ SAVANNA ]


def Test_FetchOffDisplayExhibitNames_TestForSeasonOnly_ExpectSeasonExhibitsOnly(
      off_display_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_status(
      off_display_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      start_date='2026-09-01',
      end_date=None )
   _insert_status(
      off_display_exhibit_conn,
      species=TIGER,
      exhibit=EURASIA,
      is_off_display_for_season=1,
      start_date='2026-09-01',
      end_date=None )

   off_display_exhibit_names = AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names(
      off_display_exhibit_conn,
      TODAY,
      for_season_only=True )

   assert off_display_exhibit_names == [ EURASIA ]


def Test_FetchOffDisplayExhibitNamesForSpecies_TestForSeasonOnly_ExpectSeasonExhibitsOnly(
      off_display_exhibit_conn: sqlite3.Connection ) -> None:
   _insert_status(
      off_display_exhibit_conn,
      species=LION,
      exhibit=SAVANNA,
      start_date='2026-09-01',
      end_date=None )
   _insert_status(
      off_display_exhibit_conn,
      species=LION,
      exhibit=EURASIA,
      is_off_display_for_season=1,
      start_date='2026-09-01',
      end_date=None )

   off_display_exhibit_names_for_species = AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names_for_species(
      off_display_exhibit_conn,
      TODAY,
      LION,
      for_season_only=True )

   assert off_display_exhibit_names_for_species == [ EURASIA ]
