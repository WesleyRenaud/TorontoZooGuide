from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.scheduling.items.listed_schedule_target_resolver import ListedScheduleTargetResolver


TARGET_SCHEMA = """
CREATE TABLE EnclosureViewing (
   SPECIES                              TEXT        NOT NULL,
   EXHIBIT                              TEXT        NOT NULL,
   NAME                                 TEXT,
   DEFAULT_ITINERARY_DURATION_MINUTES   REAL
);

CREATE TABLE Attraction (
   NAME                                 TEXT        NOT NULL PRIMARY KEY,
   DEFAULT_ITINERARY_DURATION_MINUTES   REAL,
   IS_ALSO_TRANSPORTATION               INTEGER     NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryAnimal (
   SPECIES                              TEXT        NOT NULL,
   EXHIBIT                              TEXT        NOT NULL,
   ENCLOSURE_NAME                       TEXT,
   START_TIME                           TEXT,
   END_TIME                             TEXT
);
"""

LION_KEY = AnimalScheduleItemKey(
   species='African Lion',
   exhibit='Africa Savanna',
)

CAROUSEL_KEY = AttractionScheduleItemKey( name='Conservation Carousel' )


@pytest.fixture
def target_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( TARGET_SCHEMA )
   conn.execute(
      """   INSERT INTO EnclosureViewing (
               SPECIES,
               EXHIBIT,
               NAME,
               DEFAULT_ITINERARY_DURATION_MINUTES
            )
            VALUES ( ?, ?, NULL, ? );
      """,
      ( 'African Lion', 'Africa Savanna', 8 ) )
   conn.execute(
      """   INSERT INTO Attraction (
               NAME,
               DEFAULT_ITINERARY_DURATION_MINUTES,
               IS_ALSO_TRANSPORTATION
            )
            VALUES ( ?, ?, 0 );
      """,
      ( 'Conservation Carousel', 12 ) )
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, NULL, NULL, NULL );
      """,
      ( 'African Lion', 'Africa Savanna' ) )
   conn.commit()

   yield conn

   conn.close()


def Test_Resolve_TestAnimalDefault_ExpectEnclosureDuration(
      target_conn: sqlite3.Connection ) -> None:
   target = ListedScheduleTargetResolver.resolve( target_conn, LION_KEY )

   assert target.default_duration_seconds == 8 * 60


def Test_Resolve_TestAttractionDefault_ExpectAttractionDuration(
      target_conn: sqlite3.Connection ) -> None:
   target = ListedScheduleTargetResolver.resolve( target_conn, CAROUSEL_KEY )

   assert target.default_duration_seconds == 12 * 60


def Test_Apply_TestExistingAnimal_ExpectScheduleUpdated(
      target_conn: sqlite3.Connection ) -> None:
   updated = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      LION_KEY,
      '10:00 AM',
      '10:08 AM',
      insert_if_missing=False )

   assert updated

   row = target_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( 'African Lion', 'Africa Savanna' ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] == '10:00 AM'
   assert row[ 'END_TIME' ] == '10:08 AM'
