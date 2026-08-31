from __future__ import annotations

import sqlite3

import pytest

from api.attractions.data_access.attraction_animal_record import AttractionAnimalRecord
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.scheduling.bulk.attraction_animal_coverer import AttractionAnimalCoverer
from api.itinerary.scheduling.core.time_block import TimeBlock


KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'

COVERER_SCHEMA = """
CREATE TABLE AttractionAnimal (
   ATTRACTION       TEXT        NOT NULL,
   SPECIES          TEXT        NOT NULL,
   EXHIBIT          TEXT        NOT NULL,
   ENCLOSURE_NAME   TEXT,
   PRIMARY KEY ( ATTRACTION, SPECIES, EXHIBIT )
);

CREATE TABLE ItineraryAnimal (
   SPECIES              TEXT        NOT NULL,
   EXHIBIT              TEXT        NOT NULL,
   ENCLOSURE_NAME       TEXT,
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER,
   IS_ADDED             INTEGER     NOT NULL DEFAULT 0,
   COVERED_BY_TALK      INTEGER     NOT NULL DEFAULT 0,
   START_TIME           TEXT,
   END_TIME             TEXT
);
"""

KANGAROO_ROW = ItineraryAnimalRecord(
   species='Western Grey Kangaroo',
   exhibit='Australasia Outdoor',
   covered_by_talk=True,
   start_time='11:00 AM',
   end_time='11:30 AM',
)

TIGER_ROW = ItineraryAnimalRecord(
   species='Amur Tiger',
   exhibit='Eurasia Wilds',
   start_time='12:00 PM',
   end_time='12:08 PM',
)


@pytest.fixture
def coverer_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( COVERER_SCHEMA )
   conn.execute(
      """   INSERT INTO AttractionAnimal (
               ATTRACTION,
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME
            )
            VALUES ( ?, ?, ?, NULL );
      """,
      (
         KANGAROO_WALK_THRU,
         'Western Grey Kangaroo',
         'Australasia Outdoor',
      ) )
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME,
               COVERED_BY_TALK
            )
            VALUES ( ?, ?, NULL, ?, ?, 1 );
      """,
      (
         'Western Grey Kangaroo',
         'Australasia Outdoor',
         '11:00 AM',
         '11:30 AM',
      ) )
   conn.commit()

   yield conn

   conn.close()


def Test_KeysToCover_TestWalkThruAnimal_ExpectLinkedKangaroo(
      coverer_conn: sqlite3.Connection ) -> None:
   covered = AttractionAnimalCoverer.keys_to_cover(
      coverer_conn,
      [ KANGAROO_WALK_THRU ],
      [ KANGAROO_ROW, TIGER_ROW ] )

   assert len( covered ) == 1
   animal_row, attraction_name = next( iter( covered.values() ) )

   assert attraction_name == KANGAROO_WALK_THRU
   assert animal_row.species == 'Western Grey Kangaroo'


def Test_RestoreAfterRemoved_TestCoveredKangaroo_ExpectDefaultDurationSchedule(
      coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.attraction_animal_coverer.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: 5 * 60 )

   cur = coverer_conn.cursor()
   restored = AttractionAnimalCoverer.restore_after_removed(
      cur,
      coverer_conn,
      attraction_name=KANGAROO_WALK_THRU,
      attraction_block=TimeBlock(
         start_seconds=11 * 3600,
         end_seconds=11 * 3600 + 30 * 60 ),
      animal_rows=[ KANGAROO_ROW, TIGER_ROW ] )
   coverer_conn.commit()
   cur.close()

   row = coverer_conn.execute(
      """   SELECT START_TIME, END_TIME, COVERED_BY_TALK
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( 'Western Grey Kangaroo', 'Australasia Outdoor' ),
   ).fetchone()

   assert restored.replacement_end_seconds == 11 * 3600 + 5 * 60
   assert row is not None
   assert row[ 'START_TIME' ] == '11:00 AM'
   assert row[ 'END_TIME' ] == '11:05 AM'
   assert row[ 'COVERED_BY_TALK' ] == 0
