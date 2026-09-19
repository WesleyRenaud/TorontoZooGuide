from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_status_provider import AnimalStatusProvider
from api.animals.domain.animal_viewing_scope import AnimalViewingScope


SPECIES = 'Wood Bison'
EXHIBIT = 'Canadian Domain'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'Temporarily off display.'
MALE_HERD = AnimalViewingScope.from_enclosure_name( 'Male Herd' )
FEMALE_HERD = AnimalViewingScope.from_enclosure_name( 'Female Herd' )

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
def animal_status_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ANIMAL_STATUS_SCHEMA )
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


def Test_SaveAnimalOffDisplayStatus_TestSelectedEnclosures_ExpectPersistsRows(
      animal_status_conn: sqlite3.Connection ) -> None:
   assert AnimalStatusProvider.save_animal_off_display_status(
      animal_status_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scopes=[ MALE_HERD, FEMALE_HERD ],
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE ) is True

   assert _status_rows( animal_status_conn ) == [
      ( 'Female Herd', 1, START_DATE, END_DATE, MESSAGE ),
      ( 'Male Herd', 1, START_DATE, END_DATE, MESSAGE ),
   ]


def Test_SaveAnimalOffDisplayStatus_TestOneEnclosure_ExpectLeavesOtherStatus(
      animal_status_conn: sqlite3.Connection ) -> None:
   AnimalStatusProvider.save_animal_off_display_status(
      animal_status_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scopes=[ FEMALE_HERD ],
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE )

   assert AnimalStatusProvider.save_animal_off_display_status(
      animal_status_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scopes=[ MALE_HERD ],
      start_date='2026-07-01',
      end_date='2026-07-15',
      message='Male paddock closed.' ) is True

   assert _status_rows( animal_status_conn ) == [
      ( 'Female Herd', 1, START_DATE, END_DATE, MESSAGE ),
      ( 'Male Herd', 1, '2026-07-01', '2026-07-15', 'Male paddock closed.' ),
   ]


def Test_SaveAnimalOnDisplayStatus_TestSelectedEnclosures_ExpectClearsThoseStatuses(
      animal_status_conn: sqlite3.Connection ) -> None:
   AnimalStatusProvider.save_animal_off_display_status(
      animal_status_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scopes=[ MALE_HERD, FEMALE_HERD ],
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE )

   assert AnimalStatusProvider.save_animal_on_display_status(
      animal_status_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scopes=[ MALE_HERD ] ) is True

   assert _status_rows( animal_status_conn ) == [
      ( 'Female Herd', 1, START_DATE, END_DATE, MESSAGE ),
   ]


def Test_SaveAnimalOnDisplayStatus_TestNoMatchingStatus_ExpectFalse(
      animal_status_conn: sqlite3.Connection ) -> None:
   assert AnimalStatusProvider.save_animal_on_display_status(
      animal_status_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scopes=[ MALE_HERD ] ) is False
