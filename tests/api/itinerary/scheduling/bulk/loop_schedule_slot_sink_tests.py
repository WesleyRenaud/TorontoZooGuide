from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.scheduling.bulk.loop_schedule_slot_sink import LoopScheduleSlotSink
from api.itinerary.scheduling.core.time_block import TimeBlock


LION = ItineraryAnimalRecord(
   species='African Lion',
   exhibit='Africa Savanna',
   old_likelihood=None,
   new_likelihood=100,
)

CAROUSEL = ItineraryAttractionRecord(
   attraction='Conservation Carousel',
   old_likelihood=None,
   new_likelihood=100,
)

SLOT_SCHEMA = """
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

CREATE TABLE ItineraryAttraction (
   ATTRACTION           TEXT        NOT NULL PRIMARY KEY,
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER,
   START_TIME           TEXT,
   END_TIME             TEXT
);

CREATE TABLE ItineraryDate (
   ITINERARY_DATE       TEXT
);
"""


@pytest.fixture
def slot_sink_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( SLOT_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME
            )
            VALUES ( ?, ?, NULL );
      """,
      ( LION.species, LION.exhibit ) )
   conn.execute(
      'INSERT INTO ItineraryAttraction ( ATTRACTION ) VALUES ( ? );',
      ( CAROUSEL.attraction, ) )
   conn.commit()

   yield conn

   conn.close()


def Test_Save_TestPersistDisabled_ExpectSlotsRecordedAndBlockersUpdated(
      slot_sink_conn: sqlite3.Connection ) -> None:
   sink = LoopScheduleSlotSink( persist=False )
   blockers: list[ TimeBlock ] = []
   slots = [
      ( LION, '10:00 AM', '10:08 AM' ),
      ( CAROUSEL, '11:00 AM', '11:20 AM' ),
   ]

   saved = sink.save( slot_sink_conn, blockers, slots )

   assert saved is True
   assert sink.slots == slots
   assert len( blockers ) == 2
   assert blockers[ 0 ].start_seconds == 10 * 3600
   assert blockers[ 1 ].start_seconds == 11 * 3600


def Test_Save_TestPersistAnimalSlot_ExpectDatabaseUpdated(
      slot_sink_conn: sqlite3.Connection ) -> None:
   sink = LoopScheduleSlotSink( persist=True )
   blockers: list[ TimeBlock ] = []

   saved = sink.save(
      slot_sink_conn,
      blockers,
      [ ( LION, '10:00 AM', '10:08 AM' ) ] )

   row = slot_sink_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?;
      """,
      ( LION.species, ),
   ).fetchone()

   assert saved is True
   assert row is not None
   assert row[ 'START_TIME' ] == '10:00 AM'
   assert row[ 'END_TIME' ] == '10:08 AM'
   assert len( blockers ) == 1
