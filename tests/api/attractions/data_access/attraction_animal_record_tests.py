from __future__ import annotations

import sqlite3

import pytest

from api.animals.search.species_exhibit_key import SpeciesExhibitKey
from api.attractions.data_access.attraction_animal_record import AttractionAnimalRecord
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.scheduling.bulk.attraction_animal_coverer import AttractionAnimalCoverer
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.models.animal_diff import AnimalDiff





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

CREATE TABLE ItineraryAttraction (
   ATTRACTION           TEXT        NOT NULL PRIMARY KEY,
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER,
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

UNCOVERED_KANGAROO_ROW = ItineraryAnimalRecord(
   species='Western Grey Kangaroo',
   exhibit='Australasia Outdoor',
   new_likelihood=100,
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


@pytest.fixture
def apply_coverer_conn() -> sqlite3.Connection:
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
               NEW_LIKELIHOOD,
               COVERED_BY_TALK
            )
            VALUES ( ?, ?, NULL, 100, 0 );
      """,
      (
         'Western Grey Kangaroo',
         'Australasia Outdoor',
      ) )
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               NEW_LIKELIHOOD,
               START_TIME,
               END_TIME,
               COVERED_BY_TALK
            )
            VALUES ( ?, ?, NULL, 100, ?, ?, 0 );
      """,
      (
         'Amur Tiger',
         'Eurasia Wilds',
         '12:00 PM',
         '12:08 PM',
      ) )
   conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               NEW_LIKELIHOOD,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, 100, ?, ? );
      """,
      (
         KANGAROO_WALK_THRU,
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


def Test_Apply_TestScheduledWalkThru_ExpectKangarooCoveredWithAttractionTimes(
      apply_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.attraction_animal_coverer.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:00 AM',
         departure_time='5:00 PM',
         attraction_rows=[
            ItineraryAttractionRecord(
               attraction=KANGAROO_WALK_THRU,
               old_likelihood=None,
               new_likelihood=100,
               start_time='11:00 AM',
               end_time='11:30 AM',
            ),
         ],
      ) )

   covered = AttractionAnimalCoverer.keys_to_cover(
      apply_coverer_conn,
      [ KANGAROO_WALK_THRU ],
      [ UNCOVERED_KANGAROO_ROW, TIGER_ROW ],
   )

   AttractionAnimalCoverer.apply( apply_coverer_conn, covered )

   kangaroo = apply_coverer_conn.execute(
      """   SELECT COVERED_BY_TALK, START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( 'Western Grey Kangaroo', 'Australasia Outdoor' ),
   ).fetchone()
   tiger = apply_coverer_conn.execute(
      """   SELECT COVERED_BY_TALK, START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( 'Amur Tiger', 'Eurasia Wilds' ),
   ).fetchone()

   assert kangaroo is not None
   assert kangaroo[ 'COVERED_BY_TALK' ] == 1
   assert kangaroo[ 'START_TIME' ] == '11:00 AM'
   assert kangaroo[ 'END_TIME' ] == '11:30 AM'
   assert tiger is not None
   assert tiger[ 'COVERED_BY_TALK' ] == 0
   assert tiger[ 'START_TIME' ] == '12:00 PM'


def Test_Apply_TestEmptyCoveredMap_ExpectNoop(
      apply_coverer_conn: sqlite3.Connection ) -> None:
   AttractionAnimalCoverer.apply( apply_coverer_conn, {} )

   kangaroo = apply_coverer_conn.execute(
      """   SELECT COVERED_BY_TALK
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( 'Western Grey Kangaroo', 'Australasia Outdoor' ),
   ).fetchone()

   assert kangaroo is not None
   assert kangaroo[ 'COVERED_BY_TALK' ] == 0


def Test_Apply_TestMissingAttractionSchedule_ExpectSkip(
      apply_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.attraction_animal_coverer.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:00 AM',
         departure_time='5:00 PM',
         attraction_rows=[],
      ) )

   covered = AttractionAnimalCoverer.keys_to_cover(
      apply_coverer_conn,
      [ KANGAROO_WALK_THRU ],
      [ UNCOVERED_KANGAROO_ROW ],
   )

   AttractionAnimalCoverer.apply( apply_coverer_conn, covered )

   kangaroo = apply_coverer_conn.execute(
      """   SELECT COVERED_BY_TALK, START_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( 'Western Grey Kangaroo', 'Australasia Outdoor' ),
   ).fetchone()

   assert kangaroo is not None
   assert kangaroo[ 'COVERED_BY_TALK' ] == 0
   assert kangaroo[ 'START_TIME' ] is None


def Test_KeysToCover_TestLinkWithoutMatchingAnimal_ExpectEmpty(
      coverer_conn: sqlite3.Connection ) -> None:
   covered = AttractionAnimalCoverer.keys_to_cover(
      coverer_conn,
      [ KANGAROO_WALK_THRU ],
      [ TIGER_ROW ] )

   assert covered == {}


def Test_RestoreAfterRemoved_TestMissingDuration_ExpectCleared(
      coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.attraction_animal_coverer.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: None )

   cur = coverer_conn.cursor()
   restored = AttractionAnimalCoverer.restore_after_removed(
      cur,
      coverer_conn,
      attraction_name=KANGAROO_WALK_THRU,
      attraction_block=TimeBlock(
         start_seconds=11 * 3600,
         end_seconds=11 * 3600 + 30 * 60 ),
      animal_rows=[ KANGAROO_ROW ] )
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

   assert restored.animals == []
   assert restored.replacement_end_seconds is None
   assert row is not None
   assert row[ 'START_TIME' ] is None
   assert row[ 'END_TIME' ] is None


def Test_UncoverForRemoved_TestCoveredAnimal_ExpectDefaultDuration(
      coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.attraction_animal_coverer.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: 8 * 60 )

   animals = [
      AnimalDiff(
         species='Western Grey Kangaroo',
         exhibit='Australasia Outdoor',
         old_likelihood=None,
         new_likelihood=100,
         covered_by_talk=True,
         start_time='11:00 AM',
         end_time='11:30 AM' ),
   ]
   removed = [
      ItineraryAttractionRecord(
         attraction=KANGAROO_WALK_THRU,
         old_likelihood=None,
         new_likelihood=100,
         start_time='11:00 AM',
         end_time='11:30 AM' ),
   ]

   result = AttractionAnimalCoverer.uncover_for_removed(
      coverer_conn,
      animals,
      removed )

   assert result[ 0 ].covered_by_talk is False
   assert result[ 0 ].start_time == '11:00 AM'
   assert result[ 0 ].end_time == '11:08 AM'


def Test_UncoverForRemoved_TestMissingDuration_ExpectClearedTimes(
      coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.attraction_animal_coverer.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: None )

   animals = [
      AnimalDiff(
         species='Western Grey Kangaroo',
         exhibit='Australasia Outdoor',
         old_likelihood=None,
         new_likelihood=100,
         covered_by_talk=True,
         start_time='11:00 AM',
         end_time='11:30 AM' ),
   ]
   removed = [
      ItineraryAttractionRecord(
         attraction=KANGAROO_WALK_THRU,
         old_likelihood=None,
         new_likelihood=100,
         start_time='11:00 AM',
         end_time='11:30 AM' ),
   ]

   result = AttractionAnimalCoverer.uncover_for_removed(
      coverer_conn,
      animals,
      removed )

   assert result[ 0 ].covered_by_talk is False
   assert result[ 0 ].start_time is None
   assert result[ 0 ].end_time is None


def Test_UncoverForRemoved_TestInvalidAttractionTimes_ExpectUncoverOnly(
      coverer_conn: sqlite3.Connection ) -> None:

   animals = [
      AnimalDiff(
         species='Western Grey Kangaroo',
         exhibit='Australasia Outdoor',
         old_likelihood=None,
         new_likelihood=100,
         covered_by_talk=True,
         start_time='11:00 AM',
         end_time='11:30 AM' ),
   ]
   removed = [
      ItineraryAttractionRecord(
         attraction=KANGAROO_WALK_THRU,
         old_likelihood=None,
         new_likelihood=100,
         start_time=None,
         end_time=None ),
   ]

   result = AttractionAnimalCoverer.uncover_for_removed(
      coverer_conn,
      animals,
      removed )

   assert result[ 0 ].covered_by_talk is False
   assert result[ 0 ].start_time is None
   assert result[ 0 ].end_time is None


def Test_RestoreAfterRemoved_TestUncoveredAnimal_ExpectSkipped(
      coverer_conn: sqlite3.Connection ) -> None:
   uncovered = ItineraryAnimalRecord(
      species='Western Grey Kangaroo',
      exhibit='Australasia Outdoor',
      covered_by_talk=False,
      start_time='11:00 AM',
      end_time='11:30 AM',
   )
   cur = coverer_conn.cursor()
   restored = AttractionAnimalCoverer.restore_after_removed(
      cur,
      coverer_conn,
      attraction_name=KANGAROO_WALK_THRU,
      attraction_block=TimeBlock(
         start_seconds=11 * 3600,
         end_seconds=11 * 3600 + 30 * 60 ),
      animal_rows=[ uncovered ] )
   cur.close()

   assert restored.animals == []
   assert restored.replacement_end_seconds is None


def Test_UncoverForRemoved_TestUncoveredAnimal_ExpectUnchanged(
      coverer_conn: sqlite3.Connection ) -> None:

   animals = [
      AnimalDiff(
         species='Western Grey Kangaroo',
         exhibit='Australasia Outdoor',
         old_likelihood=None,
         new_likelihood=100,
         covered_by_talk=False,
         start_time='11:00 AM',
         end_time='11:30 AM' ),
   ]
   removed = [
      ItineraryAttractionRecord(
         attraction=KANGAROO_WALK_THRU,
         old_likelihood=None,
         new_likelihood=100,
         start_time='11:00 AM',
         end_time='11:30 AM' ),
   ]

   result = AttractionAnimalCoverer.uncover_for_removed(
      coverer_conn,
      animals,
      removed )

   assert result[ 0 ].covered_by_talk is False
   assert result[ 0 ].start_time == '11:00 AM'
   assert result[ 0 ].end_time == '11:30 AM'


def Test_MergeKeys_TestMultipleMaps_ExpectUnion() -> None:
   merged = AttractionAnimalCoverer.merge_keys(
      { ( 'a', 'b', None ): 'one' },
      { ( 'c', 'd', None ): 'two', ( 'a', 'b', None ): 'again' },
   )

   assert merged == { ( 'a', 'b', None ), ( 'c', 'd', None ) }


def Test_SpeciesExhibitKey_TestLinkedAnimal_ExpectKey() -> None:
   record = AttractionAnimalRecord(
      attraction='Kangaroo Walk-Thru',
      species='Western Grey Kangaroo',
      exhibit='Australasia Outdoor' )

   assert record.species_exhibit_key() == SpeciesExhibitKey.from_values(
      'Western Grey Kangaroo',
      'Australasia Outdoor' )
