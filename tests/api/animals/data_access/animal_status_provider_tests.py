from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_status_provider import AnimalStatusProvider
from api.shared.enums import AnimalViewingScope


SPECIES = 'Amur Tiger'
EXHIBIT = 'Eurasia Wilds'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'Temporarily off display.'

ANIMAL_STATUS_SCHEMA = """
CREATE TABLE EnclosureViewing (
   SPECIES          TEXT NOT NULL,
   EXHIBIT          TEXT NOT NULL,
   ENCLOSURE_TYPE   TEXT NOT NULL
);

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
def animal_status_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ANIMAL_STATUS_SCHEMA )
   conn.executemany(
      """   INSERT INTO EnclosureViewing (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_TYPE
            )
            VALUES ( ?, ?, ? );
      """,
      [
         ( SPECIES, EXHIBIT, 'Indoor' ),
         ( SPECIES, EXHIBIT, 'Outdoor' ),
      ],
   )
   conn.commit()

   yield conn

   conn.close()


def _status_rows( conn: sqlite3.Connection ) -> list[ tuple ]:
   return [
      tuple( row )
      for row in conn.execute(
         """   SELECT
                  VIEWING_SCOPE,
                  IS_OFF_DISPLAY,
                  OFF_DISPLAY_START,
                  OFF_DISPLAY_END,
                  OFF_DISPLAY_MESSAGE
               FROM AnimalStatus
               WHERE SPECIES = ?
                  AND EXHIBIT = ?
               ORDER BY VIEWING_SCOPE;
         """,
         ( SPECIES, EXHIBIT ) ).fetchall()
   ]


def Test_SaveAnimalOffDisplayStatus_TestUnknownScope_ExpectFalse(
      animal_status_conn: sqlite3.Connection ) -> None:
   empty_conn = sqlite3.connect( ':memory:' )
   empty_conn.row_factory = sqlite3.Row
   empty_conn.executescript( ANIMAL_STATUS_SCHEMA )

   assert AnimalStatusProvider.save_animal_off_display_status(
      empty_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scope=AnimalViewingScope.OUTDOOR,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE ) is False

   empty_conn.close()


def Test_SaveAnimalOffDisplayStatus_TestAllScope_ExpectPersistsRow(
      animal_status_conn: sqlite3.Connection ) -> None:
   assert AnimalStatusProvider.save_animal_off_display_status(
      animal_status_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scope=AnimalViewingScope.ALL,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE ) is True

   assert _status_rows( animal_status_conn ) == [
      ( 'all', 1, START_DATE, END_DATE, MESSAGE ),
   ]


def Test_SaveAnimalOffDisplayStatus_TestOutdoorScope_ExpectReplacesAllScope(
      animal_status_conn: sqlite3.Connection ) -> None:
   AnimalStatusProvider.save_animal_off_display_status(
      animal_status_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scope=AnimalViewingScope.ALL,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE )

   assert AnimalStatusProvider.save_animal_off_display_status(
      animal_status_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scope=AnimalViewingScope.OUTDOOR,
      start_date='2026-07-01',
      end_date='2026-07-15',
      message='Outdoor only.' ) is True

   assert _status_rows( animal_status_conn ) == [
      ( 'outdoor', 1, '2026-07-01', '2026-07-15', 'Outdoor only.' ),
   ]


def Test_SaveAnimalOnDisplayStatus_TestAllScope_ExpectClearsAllStatuses(
      animal_status_conn: sqlite3.Connection ) -> None:
   AnimalStatusProvider.save_animal_off_display_status(
      animal_status_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scope=AnimalViewingScope.OUTDOOR,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE )

   assert AnimalStatusProvider.save_animal_on_display_status(
      animal_status_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scope=AnimalViewingScope.ALL ) is True

   assert _status_rows( animal_status_conn ) == []


def Test_SaveAnimalOnDisplayStatus_TestIndoorAfterAllOffDisplay_ExpectOppositeScopeRemains(
      animal_status_conn: sqlite3.Connection ) -> None:
   AnimalStatusProvider.save_animal_off_display_status(
      animal_status_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scope=AnimalViewingScope.ALL,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE )

   assert AnimalStatusProvider.save_animal_on_display_status(
      animal_status_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scope=AnimalViewingScope.INDOOR ) is True

   assert _status_rows( animal_status_conn ) == [
      ( 'outdoor', 1, START_DATE, END_DATE, MESSAGE ),
   ]


def Test_SaveAnimalOnDisplayStatus_TestUnknownScope_ExpectFalse(
      animal_status_conn: sqlite3.Connection ) -> None:
   empty_conn = sqlite3.connect( ':memory:' )
   empty_conn.row_factory = sqlite3.Row
   empty_conn.executescript( ANIMAL_STATUS_SCHEMA )

   assert AnimalStatusProvider.save_animal_on_display_status(
      empty_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scope=AnimalViewingScope.INDOOR ) is False

   empty_conn.close()
