from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_off_display_viewing_scope_provider import AnimalOffDisplayViewingScopeProvider
from api.animals.domain.animal_viewing_scope import AnimalViewingScope


TODAY = '2026-09-16'
ORANGUTAN = 'Sumatran Orangutan'
PAVILION = 'Indo-Malaya Pavilion'

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
def off_display_scope_conn() -> sqlite3.Connection:
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
      viewing_scope: str,
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


def Test_FetchOffDisplayViewingScopes_TestEmpty_ExpectEmptyList(
      off_display_scope_conn: sqlite3.Connection ) -> None:
   assert AnimalOffDisplayViewingScopeProvider.fetch_off_display_viewing_scopes(
      off_display_scope_conn,
      TODAY,
      ORANGUTAN,
      PAVILION ) == []


def Test_FetchOffDisplayViewingScopes_TestCurrentClosedEnclosures_ExpectThoseScopes(
      off_display_scope_conn: sqlite3.Connection ) -> None:
   _insert_status(
      off_display_scope_conn,
      species=ORANGUTAN,
      exhibit=PAVILION,
      viewing_scope='Outdoor',
      start_date='2026-09-01',
      end_date=None )
   _insert_status(
      off_display_scope_conn,
      species=ORANGUTAN,
      exhibit=PAVILION,
      viewing_scope='Indoor',
      start_date='2026-09-01',
      end_date='2026-09-30' )
   _insert_status(
      off_display_scope_conn,
      species=ORANGUTAN,
      exhibit=PAVILION,
      viewing_scope='Yard',
      is_off_display=0,
      start_date='2026-09-01',
      end_date=None )
   _insert_status(
      off_display_scope_conn,
      species=ORANGUTAN,
      exhibit=PAVILION,
      viewing_scope='Expired',
      start_date='2026-08-01',
      end_date='2026-09-15' )
   _insert_status(
      off_display_scope_conn,
      species='African Lion',
      exhibit='Africa Savanna',
      viewing_scope='',
      start_date='2026-09-01',
      end_date=None )

   assert AnimalOffDisplayViewingScopeProvider.fetch_off_display_viewing_scopes(
      off_display_scope_conn,
      TODAY,
      ORANGUTAN,
      PAVILION ) == [
      AnimalViewingScope.from_enclosure_name( 'Indoor' ),
      AnimalViewingScope.from_enclosure_name( 'Outdoor' ),
   ]


def Test_FetchOffDisplayViewingScopes_TestEndingToday_ExpectIncluded(
      off_display_scope_conn: sqlite3.Connection ) -> None:
   _insert_status(
      off_display_scope_conn,
      species=ORANGUTAN,
      exhibit=PAVILION,
      viewing_scope='',
      start_date='2026-09-01',
      end_date=TODAY )

   assert AnimalOffDisplayViewingScopeProvider.fetch_off_display_viewing_scopes(
      off_display_scope_conn,
      TODAY,
      ORANGUTAN,
      PAVILION ) == [
      AnimalViewingScope.from_enclosure_name( None ),
   ]
