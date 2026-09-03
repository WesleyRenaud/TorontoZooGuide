from __future__ import annotations

import sqlite3

import pytest

from api.animals.search.viewing_spot_key_builder import ViewingSpotKeyBuilder
from api.guardians.data_access.guardians_talk_animal_record import GuardiansTalkAnimalRecord
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.loop_schedule_pin import LoopSchedulePin
from api.itinerary.scheduling.bulk.guardians_talk_animal_coverer import GuardiansTalkAnimalCoverer
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.models.animal_diff import AnimalDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.shared.enums import ScheduleItemKind


CARIBOU_TALK = 'Caribou'
CARIBOU_LINK = GuardiansTalkAnimalRecord(
   talk_name=CARIBOU_TALK,
   location='Tundra Trek',
   species='Caribou',
   exhibit='Tundra Trek',
)

CARIBOU_DIFF = AnimalDiff(
   species='Caribou',
   exhibit='Tundra Trek',
   old_likelihood=100,
   new_likelihood=100,
   covered_by_talk=True,
   start_time='3:00 PM',
   end_time='3:30 PM',
)

DELETED_CARIBOU_TALK = GuardiansTalkDiff(
   name=CARIBOU_TALK,
   is_deleted=True,
   start_time='3:00 PM',
   end_time='3:30 PM',
   location='Tundra Trek',
)

PENGUIN_TALK = 'African Penguin'
LION_TALK = 'African Lion'
OTTER_TALK = 'North American River Otter'

PENGUIN_INDOOR_ROW = ItineraryAnimalRecord(
   species='African Penguin',
   exhibit='Africa Savanna',
   enclosure_name='Indoor',
   new_likelihood=100,
)

PENGUIN_OUTDOOR_ROW = ItineraryAnimalRecord(
   species='African Penguin',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
   new_likelihood=100,
)

LION_ROW = ItineraryAnimalRecord(
   species='African Lion',
   exhibit='Africa Savanna',
   enclosure_name=None,
   new_likelihood=100,
)

LION_LINK = GuardiansTalkAnimalRecord(
   talk_name=LION_TALK,
   location='Africa Savanna',
   species='African Lion',
   exhibit='Africa Savanna',
)

OTTER_OUTDOOR_ROW = ItineraryAnimalRecord(
   species='North American River Otter',
   exhibit='Americas Pavilion',
   enclosure_name='Outdoor',
   new_likelihood=100,
)

OTTER_INDOOR_ROW = ItineraryAnimalRecord(
   species='North American River Otter',
   exhibit='Americas Pavilion',
   enclosure_name='Indoor',
   new_likelihood=100,
)

COVERER_SCHEMA = """
CREATE TABLE GuardiansTalkAnimal (
   TALK_NAME        TEXT        NOT NULL,
   LOCATION         TEXT        NOT NULL,
   SPECIES          TEXT        NOT NULL,
   EXHIBIT          TEXT        NOT NULL,
   ENCLOSURE_NAME   TEXT
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


def _talk_stop( *, name: str ) -> ItineraryStop:
   return ItineraryStop(
      schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
      item_key=name,
      walk_node_ids=( 'v-0001', ),
      is_fixed_time=True,
      start_time='11:00 AM',
      end_time='11:30 AM',
   )


def _penguin_loop_pin() -> LoopSchedulePin:
   return LoopSchedulePin(
      loop_id='africa_savanna_canadian_domain',
      viewing_spot_index=1,
      stop=_talk_stop( name=PENGUIN_TALK ),
      start_seconds=11 * 3600,
      end_seconds=11 * 3600 + 30 * 60,
   )


def _lion_loop_pin() -> LoopSchedulePin:
   return LoopSchedulePin(
      loop_id='africa_savanna_canadian_domain',
      viewing_spot_index=0,
      stop=_talk_stop( name=LION_TALK ),
      start_seconds=11 * 3600,
      end_seconds=11 * 3600 + 30 * 60,
   )


def _otter_loop_pin() -> LoopSchedulePin:
   return LoopSchedulePin(
      loop_id='americas_pavilion',
      viewing_spot_index=11,
      stop=ItineraryStop(
         schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
         item_key=OTTER_TALK,
         walk_node_ids=( 'v-0001', ),
         is_fixed_time=True,
         start_time='2:00 PM',
         end_time='2:30 PM',
      ),
      start_seconds=14 * 3600,
      end_seconds=14 * 3600 + 30 * 60,
   )


@pytest.fixture
def talk_coverer_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


@pytest.fixture
def penguin_coverer_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( COVERER_SCHEMA )
   conn.execute(
      """   INSERT INTO GuardiansTalkAnimal (
               TALK_NAME,
               LOCATION,
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      (
         PENGUIN_TALK,
         'Africa Savanna',
         'African Penguin',
         'Africa Savanna',
         'Outdoor',
      ),
   )
   conn.executemany(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               NEW_LIKELIHOOD,
               COVERED_BY_TALK,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ?, 100, 0, NULL, NULL );
      """,
      [
         ( 'African Penguin', 'Africa Savanna', 'Indoor' ),
         ( 'African Penguin', 'Africa Savanna', 'Outdoor' ),
      ],
   )
   conn.commit()

   yield conn

   conn.close()


@pytest.fixture
def lion_coverer_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( COVERER_SCHEMA )
   conn.execute(
      """   INSERT INTO GuardiansTalkAnimal (
               TALK_NAME,
               LOCATION,
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME
            )
            VALUES ( ?, ?, ?, ?, NULL );
      """,
      (
         LION_TALK,
         'Africa Savanna',
         'African Lion',
         'Africa Savanna',
      ),
   )
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               NEW_LIKELIHOOD,
               COVERED_BY_TALK,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, NULL, 100, 0, NULL, NULL );
      """,
      ( 'African Lion', 'Africa Savanna' ),
   )
   conn.commit()

   yield conn

   conn.close()


@pytest.fixture
def otter_coverer_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( COVERER_SCHEMA )
   conn.execute(
      """   INSERT INTO GuardiansTalkAnimal (
               TALK_NAME,
               LOCATION,
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      (
         OTTER_TALK,
         'Americas Pavilion',
         'North American River Otter',
         'Americas Pavilion',
         'Indoor',
      ),
   )
   conn.executemany(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               NEW_LIKELIHOOD,
               COVERED_BY_TALK,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ?, 100, 0, NULL, NULL );
      """,
      [
         ( 'North American River Otter', 'Americas Pavilion', 'Outdoor' ),
         ( 'North American River Otter', 'Americas Pavilion', 'Indoor' ),
      ],
   )
   conn.commit()

   yield conn

   conn.close()


def Test_UncoverForUnavailableTalks_TestDeletedCaribouTalkCoveredAnimal_ExpectThreeMinuteWindow(
      talk_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ CARIBOU_LINK ] if talk_name == CARIBOU_TALK else [] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: 3 * 60 )

   animals = [
      AnimalDiff(
         species=CARIBOU_DIFF.species,
         exhibit=CARIBOU_DIFF.exhibit,
         old_likelihood=CARIBOU_DIFF.old_likelihood,
         new_likelihood=CARIBOU_DIFF.new_likelihood,
         covered_by_talk=CARIBOU_DIFF.covered_by_talk,
         start_time=CARIBOU_DIFF.start_time,
         end_time=CARIBOU_DIFF.end_time,
      ),
   ]

   result = GuardiansTalkAnimalCoverer.uncover_for_unavailable_talks(
      talk_coverer_conn,
      animals,
      [ DELETED_CARIBOU_TALK ],
   )

   assert result[ 0 ].covered_by_talk is False
   assert result[ 0 ].start_time == '3:00 PM'
   assert result[ 0 ].end_time == '3:03 PM'


def Test_UncoverForUnavailableTalks_TestDeletedTalkWithoutEnclosureDuration_ExpectScheduleCleared(
      talk_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ CARIBOU_LINK ] if talk_name == CARIBOU_TALK else [] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: None )

   animals = [
      AnimalDiff(
         species=CARIBOU_DIFF.species,
         exhibit=CARIBOU_DIFF.exhibit,
         old_likelihood=CARIBOU_DIFF.old_likelihood,
         new_likelihood=CARIBOU_DIFF.new_likelihood,
         covered_by_talk=CARIBOU_DIFF.covered_by_talk,
         start_time=CARIBOU_DIFF.start_time,
         end_time=CARIBOU_DIFF.end_time,
      ),
   ]

   result = GuardiansTalkAnimalCoverer.uncover_for_unavailable_talks(
      talk_coverer_conn,
      animals,
      [ DELETED_CARIBOU_TALK ],
   )

   assert result[ 0 ].covered_by_talk is False
   assert result[ 0 ].start_time is None
   assert result[ 0 ].end_time is None


def Test_KeysToCover_TestPenguinOutdoorLoopPin_ExpectOutdoorRowOnly(
      penguin_coverer_conn: sqlite3.Connection ) -> None:
   covered = GuardiansTalkAnimalCoverer.keys_to_cover(
      penguin_coverer_conn,
      [ _penguin_loop_pin() ],
      [ PENGUIN_INDOOR_ROW, PENGUIN_OUTDOOR_ROW ],
   )

   assert set( covered ) == {
      ViewingSpotKeyBuilder.from_values(
         'African Penguin',
         'Africa Savanna',
         'Outdoor' ),
   }


def Test_ApplyAndRestore_TestPenguinOutdoor_ExpectIndoorUntouched(
      penguin_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: 5 * 60 )

   covered = GuardiansTalkAnimalCoverer.keys_to_cover(
      penguin_coverer_conn,
      [ _penguin_loop_pin() ],
      [ PENGUIN_INDOOR_ROW, PENGUIN_OUTDOOR_ROW ],
   )

   GuardiansTalkAnimalCoverer.apply( penguin_coverer_conn, covered )

   rows_by_enclosure = {
      row[ 'ENCLOSURE_NAME' ]: row
      for row in penguin_coverer_conn.execute(
         """   SELECT ENCLOSURE_NAME, COVERED_BY_TALK, START_TIME, END_TIME
               FROM ItineraryAnimal
               WHERE SPECIES = 'African Penguin';
         """,
      ).fetchall()
   }

   assert rows_by_enclosure[ 'Outdoor' ][ 'COVERED_BY_TALK' ] == 1
   assert rows_by_enclosure[ 'Outdoor' ][ 'START_TIME' ] == '11:00 AM'
   assert rows_by_enclosure[ 'Outdoor' ][ 'END_TIME' ] == '11:30 AM'
   assert rows_by_enclosure[ 'Indoor' ][ 'COVERED_BY_TALK' ] == 0
   assert rows_by_enclosure[ 'Indoor' ][ 'START_TIME' ] is None

   cur = penguin_coverer_conn.cursor()
   restored = GuardiansTalkAnimalCoverer.restore_after_removed(
      cur,
      penguin_coverer_conn,
      talk_name=PENGUIN_TALK,
      talk_block=TimeBlock(
         start_seconds=11 * 3600,
         end_seconds=11 * 3600 + 30 * 60,
      ),
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Penguin',
            exhibit='Africa Savanna',
            enclosure_name='Indoor',
            covered_by_talk=False,
         ),
         ItineraryAnimalRecord(
            species='African Penguin',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor',
            covered_by_talk=True,
            start_time='11:00 AM',
            end_time='11:30 AM',
         ),
      ],
   )
   penguin_coverer_conn.commit()
   cur.close()

   assert len( restored.animals ) == 1
   assert restored.animals[ 0 ].enclosure_name == 'Outdoor'
   assert restored.replacement_end_seconds == 11 * 3600 + 5 * 60

   rows_by_enclosure = {
      row[ 'ENCLOSURE_NAME' ]: row
      for row in penguin_coverer_conn.execute(
         """   SELECT ENCLOSURE_NAME, COVERED_BY_TALK, START_TIME, END_TIME
               FROM ItineraryAnimal
               WHERE SPECIES = 'African Penguin';
         """,
      ).fetchall()
   }

   assert rows_by_enclosure[ 'Outdoor' ][ 'COVERED_BY_TALK' ] == 0
   assert rows_by_enclosure[ 'Outdoor' ][ 'START_TIME' ] == '11:00 AM'
   assert rows_by_enclosure[ 'Outdoor' ][ 'END_TIME' ] == '11:05 AM'
   assert rows_by_enclosure[ 'Indoor' ][ 'COVERED_BY_TALK' ] == 0


def Test_KeysToCover_TestOtterIndoorLoopPin_ExpectIndoorRowOnly(
      otter_coverer_conn: sqlite3.Connection ) -> None:
   covered = GuardiansTalkAnimalCoverer.keys_to_cover(
      otter_coverer_conn,
      [ _otter_loop_pin() ],
      [ OTTER_OUTDOOR_ROW, OTTER_INDOOR_ROW ],
   )

   assert set( covered ) == {
      ViewingSpotKeyBuilder.from_values(
         'North American River Otter',
         'Americas Pavilion',
         'Indoor' ),
   }


def Test_ApplyAndRestore_TestOtterIndoor_ExpectOutdoorUntouched(
      otter_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: 5 * 60 )

   covered = GuardiansTalkAnimalCoverer.keys_to_cover(
      otter_coverer_conn,
      [ _otter_loop_pin() ],
      [ OTTER_OUTDOOR_ROW, OTTER_INDOOR_ROW ],
   )

   GuardiansTalkAnimalCoverer.apply( otter_coverer_conn, covered )

   rows_by_enclosure = {
      row[ 'ENCLOSURE_NAME' ]: row
      for row in otter_coverer_conn.execute(
         """   SELECT ENCLOSURE_NAME, COVERED_BY_TALK, START_TIME, END_TIME
               FROM ItineraryAnimal
               WHERE SPECIES = 'North American River Otter';
         """,
      ).fetchall()
   }

   assert rows_by_enclosure[ 'Indoor' ][ 'COVERED_BY_TALK' ] == 1
   assert rows_by_enclosure[ 'Indoor' ][ 'START_TIME' ] == '2:00 PM'
   assert rows_by_enclosure[ 'Indoor' ][ 'END_TIME' ] == '2:30 PM'
   assert rows_by_enclosure[ 'Outdoor' ][ 'COVERED_BY_TALK' ] == 0
   assert rows_by_enclosure[ 'Outdoor' ][ 'START_TIME' ] is None


def Test_KeysToCover_TestAfricanLionLoopPin_ExpectLionRowOnly(
      lion_coverer_conn: sqlite3.Connection ) -> None:
   covered = GuardiansTalkAnimalCoverer.keys_to_cover(
      lion_coverer_conn,
      [ _lion_loop_pin() ],
      [ LION_ROW ],
   )

   assert set( covered ) == {
      ViewingSpotKeyBuilder.from_values(
         'African Lion',
         'Africa Savanna',
         None ),
   }


def Test_ApplyAndRestore_TestAfricanLion_ExpectEightMinuteWindow(
      lion_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ LION_LINK ] if talk_name == LION_TALK else [] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: 8 * 60 )

   covered = GuardiansTalkAnimalCoverer.keys_to_cover(
      lion_coverer_conn,
      [ _lion_loop_pin() ],
      [ LION_ROW ],
   )
   GuardiansTalkAnimalCoverer.apply( lion_coverer_conn, covered )

   row = lion_coverer_conn.execute(
      """   SELECT COVERED_BY_TALK, START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = 'African Lion';
      """,
   ).fetchone()

   assert row is not None
   assert row[ 'COVERED_BY_TALK' ] == 1
   assert row[ 'START_TIME' ] == '11:00 AM'
   assert row[ 'END_TIME' ] == '11:30 AM'

   cur = lion_coverer_conn.cursor()
   restored = GuardiansTalkAnimalCoverer.restore_after_removed(
      cur,
      lion_coverer_conn,
      talk_name=LION_TALK,
      talk_block=TimeBlock(
         start_seconds=11 * 3600,
         end_seconds=11 * 3600 + 30 * 60,
      ),
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            covered_by_talk=True,
            start_time='11:00 AM',
            end_time='11:30 AM',
         ),
      ],
   )
   lion_coverer_conn.commit()
   cur.close()

   assert len( restored.animals ) == 1
   assert restored.replacement_end_seconds == 11 * 3600 + 8 * 60

   row = lion_coverer_conn.execute(
      """   SELECT COVERED_BY_TALK, START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = 'African Lion';
      """,
   ).fetchone()

   assert row is not None
   assert row[ 'COVERED_BY_TALK' ] == 0
   assert row[ 'START_TIME' ] == '11:00 AM'
   assert row[ 'END_TIME' ] == '11:08 AM'


def Test_KeysToCover_TestLinkWithoutMatchingAnimalRow_ExpectEmpty(
      lion_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ LION_LINK ] if talk_name == LION_TALK else [] )

   covered = GuardiansTalkAnimalCoverer.keys_to_cover(
      lion_coverer_conn,
      [ _lion_loop_pin() ],
      [ PENGUIN_OUTDOOR_ROW ],
   )

   assert covered == {}


def Test_Apply_TestEmptyCoveredDict_ExpectNoDatabaseChange(
      lion_coverer_conn: sqlite3.Connection ) -> None:
   GuardiansTalkAnimalCoverer.apply( lion_coverer_conn, {} )

   row = lion_coverer_conn.execute(
      """   SELECT COVERED_BY_TALK, START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = 'African Lion';
      """,
   ).fetchone()

   assert row is not None
   assert row[ 'COVERED_BY_TALK' ] == 0
   assert row[ 'START_TIME' ] is None


def Test_UncoverForTalk_TestCoveredAnimal_ExpectScheduleCleared(
      lion_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ LION_LINK ] if talk_name == LION_TALK else [] )
   covered = GuardiansTalkAnimalCoverer.keys_to_cover(
      lion_coverer_conn,
      [ _lion_loop_pin() ],
      [ LION_ROW ],
   )
   GuardiansTalkAnimalCoverer.apply( lion_coverer_conn, covered )

   cur = lion_coverer_conn.cursor()
   uncovered = GuardiansTalkAnimalCoverer.uncover_for_talk(
      cur,
      lion_coverer_conn,
      talk_name=LION_TALK,
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            covered_by_talk=True,
            start_time='11:00 AM',
            end_time='11:30 AM',
         ),
      ],
   )
   lion_coverer_conn.commit()
   cur.close()

   assert len( uncovered ) == 1
   row = lion_coverer_conn.execute(
      """   SELECT COVERED_BY_TALK, START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = 'African Lion';
      """,
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] is None
   assert row[ 'END_TIME' ] is None


def Test_UncoverForTalk_TestNotCoveredAnimal_ExpectEmpty(
      lion_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ LION_LINK ] if talk_name == LION_TALK else [] )

   cur = lion_coverer_conn.cursor()
   uncovered = GuardiansTalkAnimalCoverer.uncover_for_talk(
      cur,
      lion_coverer_conn,
      talk_name=LION_TALK,
      animal_rows=[ LION_ROW ],
   )
   cur.close()

   assert uncovered == []


def Test_RestoreAfterRemoved_TestMissingDuration_ExpectScheduleCleared(
      lion_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ LION_LINK ] if talk_name == LION_TALK else [] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: None )
   covered = GuardiansTalkAnimalCoverer.keys_to_cover(
      lion_coverer_conn,
      [ _lion_loop_pin() ],
      [ LION_ROW ],
   )
   GuardiansTalkAnimalCoverer.apply( lion_coverer_conn, covered )

   cur = lion_coverer_conn.cursor()
   restored = GuardiansTalkAnimalCoverer.restore_after_removed(
      cur,
      lion_coverer_conn,
      talk_name=LION_TALK,
      talk_block=TimeBlock(
         start_seconds=11 * 3600,
         end_seconds=11 * 3600 + 30 * 60,
      ),
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            covered_by_talk=True,
            start_time='11:00 AM',
            end_time='11:30 AM',
         ),
      ],
   )
   lion_coverer_conn.commit()
   cur.close()

   assert restored.animals == []
   assert restored.replacement_end_seconds is None
   row = lion_coverer_conn.execute(
      """   SELECT COVERED_BY_TALK, START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = 'African Lion';
      """,
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] is None
   assert row[ 'END_TIME' ] is None


def Test_UncoverForUnavailableTalks_TestActiveTalk_ExpectNoChange(
      talk_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ CARIBOU_LINK ] )

   animals = [
      AnimalDiff(
         species='Caribou',
         exhibit='Tundra Trek',
         old_likelihood=100,
         new_likelihood=100,
         covered_by_talk=True,
         start_time='3:00 PM',
         end_time='3:30 PM',
      ),
   ]
   result = GuardiansTalkAnimalCoverer.uncover_for_unavailable_talks(
      talk_coverer_conn,
      animals,
      [
         GuardiansTalkDiff(
            name=CARIBOU_TALK,
            is_deleted=False,
            start_time='3:00 PM',
            end_time='3:30 PM',
            location='Tundra Trek',
         ),
      ],
   )

   assert result[ 0 ].covered_by_talk is True
   assert result[ 0 ].start_time == '3:00 PM'


def Test_UncoverForUnavailableTalks_TestDeletedTalkInvalidTimes_ExpectNoChange(
      talk_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ CARIBOU_LINK ] )

   animals = [
      AnimalDiff(
         species='Caribou',
         exhibit='Tundra Trek',
         old_likelihood=100,
         new_likelihood=100,
         covered_by_talk=True,
         start_time='3:00 PM',
         end_time='3:30 PM',
      ),
   ]
   result = GuardiansTalkAnimalCoverer.uncover_for_unavailable_talks(
      talk_coverer_conn,
      animals,
      [
         GuardiansTalkDiff(
            name=CARIBOU_TALK,
            is_deleted=True,
            start_time=None,
            end_time=None,
            location='Tundra Trek',
         ),
      ],
   )

   assert result[ 0 ].covered_by_talk is True


def Test_UncoverForUnavailableTalks_TestDeletedTalkUnlinkedAnimal_ExpectNoChange(
      talk_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ CARIBOU_LINK ] )

   animals = [
      AnimalDiff(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=100,
         new_likelihood=100,
         covered_by_talk=True,
         start_time='11:00 AM',
         end_time='11:30 AM',
      ),
   ]
   result = GuardiansTalkAnimalCoverer.uncover_for_unavailable_talks(
      talk_coverer_conn,
      animals,
      [ DELETED_CARIBOU_TALK ],
   )

   assert result[ 0 ].covered_by_talk is True
   assert result[ 0 ].start_time == '11:00 AM'


def Test_RestoreAfterRemoved_TestUncoveredLinkedAnimal_ExpectSkipped(
      lion_coverer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.guardians_talk_animal_coverer.GuardiansTalkAnimalProvider.fetch_animal_links',
      lambda conn, talk_name: [ LION_LINK ] if talk_name == LION_TALK else [] )

   cur = lion_coverer_conn.cursor()
   restored = GuardiansTalkAnimalCoverer.restore_after_removed(
      cur,
      lion_coverer_conn,
      talk_name=LION_TALK,
      talk_block=TimeBlock(
         start_seconds=11 * 3600,
         end_seconds=11 * 3600 + 30 * 60,
      ),
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            covered_by_talk=False,
         ),
      ],
   )
   cur.close()

   assert restored.animals == []
   assert restored.replacement_end_seconds is None
