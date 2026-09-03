from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.data_access.itinerary_transportation_provider import ItineraryTransportationProvider
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.schedule_itinerary_item_provider import ScheduleItineraryItemProvider
from api.itinerary.data_access.schedule_itinerary_transportation_provider import ScheduleItineraryTransportationProvider
from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.core.time_block_builder import TimeBlockBuilder
from api.itinerary.scheduling.unscheduling.guest_schedule_shift_applier import GuestScheduleShiftApplier
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.enums import ItineraryEventType


CHEETAH_KEY = AnimalScheduleItemKey(
   species='Cheetah',
   exhibit='Africa Savanna',
)

ZOOMOBILE = 'Zoomobile'
ZOOMOBILE_ATTRACTION_START = '11:00 AM'
ZOOMOBILE_ATTRACTION_END = '11:30 AM'
ZOOMOBILE_TRANSIT_START = '11:30 AM'
ZOOMOBILE_TRANSIT_END = '12:00 PM'
ZOOMOBILE_TRANSIT_ROUTE = 'zoomobile-route'
ZEBRA_TALK = "Grevy's Zebra"
CAMEL_TALK = 'Bactrian Camel'
ZEBRA_TALK_KEY = GuardiansTalkScheduleItemKey(
   name=ZEBRA_TALK,
   start_time='12:00' )

SHIFT_APPLIER_SCHEMA = """
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

CREATE TABLE ItineraryTransportation (
   TRANSPORTATION           TEXT        NOT NULL,
   OLD_LIKELIHOOD           INTEGER,
   NEW_LIKELIHOOD           INTEGER,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   START_TIME               TEXT,
   END_TIME                 TEXT,
   ROUTE                    TEXT,
   BULK_TRANSIT_EVALUATED   INTEGER     NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryTransportationLeg (
   TRANSPORTATION           TEXT        NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   FROM_STATION             TEXT        NOT NULL,
   TO_STATION               TEXT        NOT NULL,
   START_TIME               TEXT        NOT NULL,
   END_TIME                 TEXT        NOT NULL
);

CREATE TABLE ItineraryTransportationRouteMarker (
   TRANSPORTATION           TEXT        NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   SEQUENCE                 INTEGER     NOT NULL,
   MARKER_ORDER             INTEGER     NOT NULL,
   MARKER_ID                TEXT        NOT NULL
);

CREATE TABLE ItineraryEvent (
   EVENT_TYPE           TEXT        NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT
);

CREATE TABLE ItineraryGuardiansTalk (
   TALK_NAME            TEXT        NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT,
   IS_DELETED           INTEGER     NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryWildEncounter (
   WILD_ENCOUNTER       TEXT        NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT,
   IS_DELETED           INTEGER     NOT NULL DEFAULT 0
);
"""


@pytest.fixture
def shift_applier_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( SHIFT_APPLIER_SCHEMA )

   yield conn

   conn.close()


def _insert_three_animal_schedule(
      conn: sqlite3.Connection,
      *,
      penguin_start: str,
      penguin_end: str ) -> SavedItinerary:
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, NULL, ?, ? );
      """,
      ( 'African Lion', 'Africa Savanna', '10:00 AM', '10:15 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, NULL, ?, ? );
      """,
      ( 'Cheetah', 'Africa Savanna', '10:17 AM', '10:32 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      ( 'African Penguin', 'Africa Savanna', 'Outdoor', penguin_start, penguin_end ) )
   conn.commit()

   return SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:15 AM',
         ),
         ItineraryAnimalRecord(
            species='Cheetah',
            exhibit='Africa Savanna',
            start_time='10:17 AM',
            end_time='10:32 AM',
         ),
         ItineraryAnimalRecord(
            species='African Penguin',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor',
            start_time=penguin_start,
            end_time=penguin_end,
         ),
      ],
   )


def _insert_zoomobile_transportation_schedule( conn: sqlite3.Connection ) -> SavedItinerary:
   conn.execute(
      """   INSERT INTO ItineraryTransportation (
               TRANSPORTATION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               ADDED_AS_ATTRACTION,
               START_TIME,
               END_TIME,
               ROUTE,
               BULK_TRANSIT_EVALUATED
            )
            VALUES ( ?, NULL, 3, 1, ?, ?, NULL, 0 );
      """,
      ( ZOOMOBILE, ZOOMOBILE_ATTRACTION_START, ZOOMOBILE_ATTRACTION_END ) )
   conn.execute(
      """   INSERT INTO ItineraryTransportation (
               TRANSPORTATION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               ADDED_AS_ATTRACTION,
               START_TIME,
               END_TIME,
               ROUTE,
               BULK_TRANSIT_EVALUATED
            )
            VALUES ( ?, NULL, 3, 0, ?, ?, ?, 1 );
      """,
      (
         ZOOMOBILE,
         ZOOMOBILE_TRANSIT_START,
         ZOOMOBILE_TRANSIT_END,
         ZOOMOBILE_TRANSIT_ROUTE,
      ) )
   conn.execute(
      """   INSERT INTO ItineraryTransportationLeg (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION,
               FROM_STATION,
               TO_STATION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, 0, ?, ?, ?, ? );
      """,
      ( ZOOMOBILE, 'Station A', 'Station B', '11:30 AM', '11:45 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryTransportationLeg (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION,
               FROM_STATION,
               TO_STATION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, 0, ?, ?, ?, ? );
      """,
      ( ZOOMOBILE, 'Station B', 'Station C', '11:45 AM', '12:00 PM' ) )
   conn.commit()

   return SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      transportation_rows=(
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=True,
            start_time=ZOOMOBILE_ATTRACTION_START,
            end_time=ZOOMOBILE_ATTRACTION_END,
         ),
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=False,
            start_time=ZOOMOBILE_TRANSIT_START,
            end_time=ZOOMOBILE_TRANSIT_END,
            route=ZOOMOBILE_TRANSIT_ROUTE,
            bulk_transit_evaluated=True,
            legs=[
               ItineraryTransportationLeg(
                  transportation=ZOOMOBILE,
                  added_as_attraction=False,
                  from_station='Station A',
                  to_station='Station B',
                  start_time='11:30 AM',
                  end_time='11:45 AM',
               ),
               ItineraryTransportationLeg(
                  transportation=ZOOMOBILE,
                  added_as_attraction=False,
                  from_station='Station B',
                  to_station='Station C',
                  start_time='11:45 AM',
                  end_time='12:00 PM',
               ),
            ],
         ),
      ),
   )


def _insert_adjacent_talk_unschedule_fixture(
      conn: sqlite3.Connection,
      *,
      include_camel_talk: bool ) -> SavedItinerary:
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      ( 'Masai Giraffe', 'Africa Savanna', 'Outdoor', '1:00 PM', '1:10 PM' ) )
   conn.execute(
      """   INSERT INTO ItineraryGuardiansTalk (
               TALK_NAME,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES ( ?, ?, ?, 0 );
      """,
      ( ZEBRA_TALK, '12:00 PM', '12:30 PM' ) )

   if include_camel_talk:
      conn.execute(
         """   INSERT INTO ItineraryGuardiansTalk (
                  TALK_NAME,
                  START_TIME,
                  END_TIME,
                  IS_DELETED
               )
               VALUES ( ?, ?, ?, 0 );
         """,
         ( CAMEL_TALK, '12:30 PM', '1:00 PM' ) )

   conn.commit()

   return SavedItinerary(
      date_value='2026-07-01',
      arrival_time='9:00 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor',
            start_time='1:00 PM',
            end_time='1:10 PM',
         ),
      ],
      guardians_talk_rows=[
         ItineraryGuardiansTalkRecord(
            talk_name=ZEBRA_TALK,
            start_time='12:00 PM',
            end_time='12:30 PM',
            is_deleted=False,
         ),
         *(
            [
               ItineraryGuardiansTalkRecord(
                  talk_name=CAMEL_TALK,
                  start_time='12:30 PM',
                  end_time='1:00 PM',
                  is_deleted=False,
               ),
            ]
            if include_camel_talk
            else []
         ),
      ],
   )


def Test_ShiftedScheduleTimes_TestNegativeShift_ExpectEarlierBlock() -> None:
   shifted = GuestScheduleShiftApplier.shifted_schedule_times( '10:45 AM', '11:00 AM', -15 * 60 )

   assert shifted == ( '10:30 AM', '10:45 AM' )


def Test_ShiftedScheduleTimes_TestInvalidShift_ExpectNone() -> None:
   assert GuestScheduleShiftApplier.shifted_schedule_times( '10:00 AM', '10:15 AM', -11 * 3600 ) is None


def Test_ResolveUnscheduledItemTimeBlock_TestAnimal_ExpectAnimalBlock() -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time=None,
      departure_time=None,
      animal_rows=(
         ItineraryAnimalRecord(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            start_time='10:15 AM',
            end_time='10:30 AM',
         ),
      ),
      attraction_rows=(),
      guardians_talk_rows=(),
      wild_encounter_rows=(),
   )

   block = GuestScheduleShiftApplier.resolve_unscheduled_item_time_block(
      saved_itinerary,
      AnimalScheduleItemKey(
         species='Masai Giraffe',
         exhibit='Africa Savanna',
      ),
   )

   assert block == TimeBlock(
      start_seconds=10 * 3600 + 15 * 60,
      end_seconds=10 * 3600 + 30 * 60,
   )


def Test_ResolveUnscheduledItemTimeBlock_TestAttraction_ExpectAttractionBlock() -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time=None,
      departure_time=None,
      animal_rows=(),
      attraction_rows=(
         ItineraryAttractionRecord(
            attraction='Conservation Carousel',
            old_likelihood=None,
            new_likelihood=None,
            start_time='1:00 PM',
            end_time='1:15 PM',
         ),
      ),
      guardians_talk_rows=(),
      wild_encounter_rows=(),
   )

   block = GuestScheduleShiftApplier.resolve_unscheduled_item_time_block(
      saved_itinerary,
      AttractionScheduleItemKey( name='Conservation Carousel' ),
   )

   assert block == TimeBlock(
      start_seconds=13 * 3600,
      end_seconds=13 * 3600 + 15 * 60,
   )


def Test_ResolveUnscheduledItemTimeBlock_TestEvent_ExpectEventBlock() -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time=None,
      departure_time=None,
      animal_rows=(),
      attraction_rows=(),
      guardians_talk_rows=(),
      wild_encounter_rows=(),
      event_rows=(
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time='12:00 PM',
            end_time='12:30 PM',
         ),
      ),
   )

   block = GuestScheduleShiftApplier.resolve_unscheduled_item_time_block(
      saved_itinerary,
      ItineraryEventType.LUNCH,
   )

   assert block == TimeBlock(
      start_seconds=12 * 3600,
      end_seconds=12 * 3600 + 30 * 60,
   )


def Test_ApplyForUnschedule_TestMiddleAnimal_ExpectLaterItemsShiftedEarlier(
      shift_applier_conn: sqlite3.Connection ) -> None:
   saved_itinerary = _insert_three_animal_schedule(
      shift_applier_conn,
      penguin_start='10:47 AM',
      penguin_end='11:02 AM' )
   cur = shift_applier_conn.cursor()

   GuestScheduleShiftApplier.apply_for_unschedule(
      shift_applier_conn,
      cur,
      saved_itinerary=saved_itinerary,
      schedule_item_key=CHEETAH_KEY )
   shift_applier_conn.commit()
   cur.close()

   penguin = shift_applier_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?
              AND ENCLOSURE_NAME = ?;
      """,
      ( 'African Penguin', 'Africa Savanna', 'Outdoor' ),
   ).fetchone()

   assert penguin is not None
   assert penguin[ 'START_TIME' ] == '10:32 AM'
   assert penguin[ 'END_TIME' ] == '10:47 AM'


def Test_ApplyForUnschedule_TestMiddleAnimalWithDeliberateGap_ExpectGapPreserved(
      shift_applier_conn: sqlite3.Connection ) -> None:
   saved_itinerary = _insert_three_animal_schedule(
      shift_applier_conn,
      penguin_start='10:52 AM',
      penguin_end='11:07 AM' )
   cur = shift_applier_conn.cursor()

   GuestScheduleShiftApplier.apply_for_unschedule(
      shift_applier_conn,
      cur,
      saved_itinerary=saved_itinerary,
      schedule_item_key=CHEETAH_KEY )
   shift_applier_conn.commit()
   cur.close()

   penguin = shift_applier_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?
              AND ENCLOSURE_NAME = ?;
      """,
      ( 'African Penguin', 'Africa Savanna', 'Outdoor' ),
   ).fetchone()

   assert penguin is not None
   assert penguin[ 'START_TIME' ] == '10:37 AM'
   assert penguin[ 'END_TIME' ] == '10:52 AM'


def Test_ApplyForUnschedule_TestAttractionZoomobile_ExpectTransitLegsShiftedEarlier(
      shift_applier_conn: sqlite3.Connection ) -> None:
   saved_itinerary = _insert_zoomobile_transportation_schedule( shift_applier_conn )
   cur = shift_applier_conn.cursor()

   GuestScheduleShiftApplier.apply_for_unschedule(
      shift_applier_conn,
      cur,
      saved_itinerary=saved_itinerary,
      schedule_item_key=AttractionScheduleItemKey( name=ZOOMOBILE ) )
   shift_applier_conn.commit()
   cur.close()

   transit_row = shift_applier_conn.execute(
      """   SELECT START_TIME, END_TIME, BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 0;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()
   legs = shift_applier_conn.execute(
      """   SELECT FROM_STATION, TO_STATION, START_TIME, END_TIME
            FROM ItineraryTransportationLeg
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 0
            ORDER BY START_TIME;
      """,
      ( ZOOMOBILE, ),
   ).fetchall()

   assert transit_row is not None
   assert transit_row[ 'START_TIME' ] == '11:00 AM'
   assert transit_row[ 'END_TIME' ] == '11:30 AM'
   assert transit_row[ 'BULK_TRANSIT_EVALUATED' ] == 1
   assert len( legs ) == 2
   assert legs[ 0 ][ 'FROM_STATION' ] == 'Station A'
   assert legs[ 0 ][ 'TO_STATION' ] == 'Station B'
   assert legs[ 0 ][ 'START_TIME' ] == '11:00 AM'
   assert legs[ 0 ][ 'END_TIME' ] == '11:15 AM'
   assert legs[ 1 ][ 'FROM_STATION' ] == 'Station B'
   assert legs[ 1 ][ 'TO_STATION' ] == 'Station C'
   assert legs[ 1 ][ 'START_TIME' ] == '11:15 AM'
   assert legs[ 1 ][ 'END_TIME' ] == '11:30 AM'


def Test_ShiftItemsAfterUnschedule_TestWovenTalkRemoved_ExpectLaterAnimalShiftedEarlier(
      shift_applier_conn: sqlite3.Connection ) -> None:
   shift_applier_conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, NULL, ?, ? );
      """,
      ( 'African Lion', 'Africa Savanna', '11:00 AM', '11:08 AM' ) )
   shift_applier_conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, NULL, ?, ? );
      """,
      ( 'Cheetah', 'Africa Savanna', '11:30 AM', '11:38 AM' ) )
   shift_applier_conn.commit()
   cur = shift_applier_conn.cursor()

   GuestScheduleShiftApplier.shift_items_after_unschedule(
      shift_applier_conn,
      cur,
      anchor_end_seconds=11 * 3600 + 30 * 60,
      shift_seconds=-22 * 60,
      freed_block=TimeBlock(
         start_seconds=11 * 3600,
         end_seconds=11 * 3600 + 30 * 60,
      ) )
   shift_applier_conn.commit()
   cur.close()

   cheetah = shift_applier_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ? AND EXHIBIT = ?;
      """,
      ( 'Cheetah', 'Africa Savanna' ),
   ).fetchone()

   assert cheetah is not None
   assert cheetah[ 'START_TIME' ] == '11:08 AM'
   assert cheetah[ 'END_TIME' ] == '11:16 AM'


def Test_ApplyForUnschedule_TestZebraRemovedWithAdjacentCamel_ExpectGiraffeUnshifted(
      shift_applier_conn: sqlite3.Connection ) -> None:
   saved_itinerary = _insert_adjacent_talk_unschedule_fixture(
      shift_applier_conn,
      include_camel_talk=True )
   cur = shift_applier_conn.cursor()

   GuestScheduleShiftApplier.apply_for_unschedule(
      shift_applier_conn,
      cur,
      saved_itinerary=saved_itinerary,
      schedule_item_key=ZEBRA_TALK_KEY )
   shift_applier_conn.commit()
   cur.close()

   giraffe = shift_applier_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?
              AND ENCLOSURE_NAME = ?;
      """,
      ( 'Masai Giraffe', 'Africa Savanna', 'Outdoor' ),
   ).fetchone()

   assert giraffe is not None
   assert giraffe[ 'START_TIME' ] == '1:00 PM'
   assert giraffe[ 'END_TIME' ] == '1:10 PM'


def Test_ApplyForUnschedule_TestZebraRemovedWithoutReplacement_ExpectGiraffeShiftedEarlier(
      shift_applier_conn: sqlite3.Connection ) -> None:
   saved_itinerary = _insert_adjacent_talk_unschedule_fixture(
      shift_applier_conn,
      include_camel_talk=False )
   cur = shift_applier_conn.cursor()

   GuestScheduleShiftApplier.apply_for_unschedule(
      shift_applier_conn,
      cur,
      saved_itinerary=saved_itinerary,
      schedule_item_key=ZEBRA_TALK_KEY )
   shift_applier_conn.commit()
   cur.close()

   giraffe = shift_applier_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?
              AND ENCLOSURE_NAME = ?;
      """,
      ( 'Masai Giraffe', 'Africa Savanna', 'Outdoor' ),
   ).fetchone()

   assert giraffe is not None
   assert giraffe[ 'START_TIME' ] == '12:30 PM'
   assert giraffe[ 'END_TIME' ] == '12:40 PM'


def Test_ResolveUnscheduledItemTimeBlock_TestUnknownKey_ExpectNone() -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time=None,
      departure_time=None,
      animal_rows=(),
      attraction_rows=(),
      guardians_talk_rows=(),
      wild_encounter_rows=(),
   )

   assert GuestScheduleShiftApplier.resolve_unscheduled_item_time_block(
      saved_itinerary,
      AnimalScheduleItemKey(
         species='Missing Animal',
         exhibit='Africa Savanna',
      ),
   ) is None


def Test_ApplyForUnschedule_TestUnknownKey_ExpectNoop(
      shift_applier_conn: sqlite3.Connection ) -> None:
   shift_applier_conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, NULL, ?, ? );
      """,
      ( 'African Lion', 'Africa Savanna', '11:00 AM', '11:08 AM' ) )
   shift_applier_conn.commit()
   cur = shift_applier_conn.cursor()

   GuestScheduleShiftApplier.apply_for_unschedule(
      shift_applier_conn,
      cur,
      saved_itinerary=SavedItinerary(
         date_value='2026-06-15',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
         animal_rows=(),
      ),
      schedule_item_key=CHEETAH_KEY )
   shift_applier_conn.commit()
   cur.close()

   lion = shift_applier_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ? AND EXHIBIT = ?;
      """,
      ( 'African Lion', 'Africa Savanna' ),
   ).fetchone()

   assert lion is not None
   assert lion[ 'START_TIME' ] == '11:00 AM'
   assert lion[ 'END_TIME' ] == '11:08 AM'


def Test_ShiftItemsAfterUnschedule_TestZeroShiftSeconds_ExpectNoop(
      shift_applier_conn: sqlite3.Connection ) -> None:
   shift_applier_conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, NULL, ?, ? );
      """,
      ( 'Cheetah', 'Africa Savanna', '11:30 AM', '11:38 AM' ) )
   shift_applier_conn.commit()
   cur = shift_applier_conn.cursor()

   GuestScheduleShiftApplier.shift_items_after_unschedule(
      shift_applier_conn,
      cur,
      anchor_end_seconds=11 * 3600 + 30 * 60,
      shift_seconds=0 )
   shift_applier_conn.commit()
   cur.close()

   cheetah = shift_applier_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ? AND EXHIBIT = ?;
      """,
      ( 'Cheetah', 'Africa Savanna' ),
   ).fetchone()

   assert cheetah is not None
   assert cheetah[ 'START_TIME' ] == '11:30 AM'
   assert cheetah[ 'END_TIME' ] == '11:38 AM'


def Test_ShiftItemsAfterUnschedule_TestOverlapWithTalk_ExpectNoShift(
      shift_applier_conn: sqlite3.Connection ) -> None:
   shift_applier_conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, NULL, ?, ? );
      """,
      ( 'Cheetah', 'Africa Savanna', '12:30 PM', '12:38 PM' ) )
   shift_applier_conn.execute(
      """   INSERT INTO ItineraryGuardiansTalk (
               TALK_NAME,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES ( ?, ?, ?, 0 );
      """,
      ( CAMEL_TALK, '12:00 PM', '12:30 PM' ) )
   shift_applier_conn.commit()
   cur = shift_applier_conn.cursor()

   GuestScheduleShiftApplier.shift_items_after_unschedule(
      shift_applier_conn,
      cur,
      anchor_end_seconds=12 * 3600 + 30 * 60,
      shift_seconds=-20 * 60,
      freed_block=TimeBlock(
         start_seconds=12 * 3600,
         end_seconds=12 * 3600 + 20 * 60,
      ) )
   shift_applier_conn.commit()
   cur.close()

   cheetah = shift_applier_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ? AND EXHIBIT = ?;
      """,
      ( 'Cheetah', 'Africa Savanna' ),
   ).fetchone()

   assert cheetah is not None
   assert cheetah[ 'START_TIME' ] == '12:30 PM'
   assert cheetah[ 'END_TIME' ] == '12:38 PM'


def Test_ShiftItemsAfterUnschedule_TestLaterAttraction_ExpectShiftedEarlier(
      shift_applier_conn: sqlite3.Connection ) -> None:
   shift_applier_conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, NULL, 3, ?, ? );
      """,
      ( 'Conservation Carousel', '11:30 AM', '11:45 AM' ) )
   shift_applier_conn.commit()
   cur = shift_applier_conn.cursor()

   GuestScheduleShiftApplier.shift_items_after_unschedule(
      shift_applier_conn,
      cur,
      anchor_end_seconds=11 * 3600 + 30 * 60,
      shift_seconds=-15 * 60 )
   shift_applier_conn.commit()
   cur.close()

   attraction = shift_applier_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( 'Conservation Carousel', ),
   ).fetchone()

   assert attraction is not None
   assert attraction[ 'START_TIME' ] == '11:15 AM'
   assert attraction[ 'END_TIME' ] == '11:30 AM'


def Test_ShiftItemsAfterUnschedule_TestLunchShiftedArrivalDepartureUntouched_ExpectShiftedSchedule(
      shift_applier_conn: sqlite3.Connection ) -> None:
   shift_applier_conn.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( ItineraryEventType.ARRIVAL.value, '9:30 AM', '9:30 AM' ) )
   shift_applier_conn.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( ItineraryEventType.LUNCH.value, '12:30 PM', '1:00 PM' ) )
   shift_applier_conn.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( ItineraryEventType.DEPARTURE.value, '5:00 PM', '5:00 PM' ) )
   shift_applier_conn.commit()
   cur = shift_applier_conn.cursor()

   GuestScheduleShiftApplier.shift_items_after_unschedule(
      shift_applier_conn,
      cur,
      anchor_end_seconds=12 * 3600 + 30 * 60,
      shift_seconds=-20 * 60 )
   shift_applier_conn.commit()
   cur.close()

   events = {
      row[ 'EVENT_TYPE' ]: ( row[ 'START_TIME' ], row[ 'END_TIME' ] )
      for row in shift_applier_conn.execute(
         """   SELECT EVENT_TYPE, START_TIME, END_TIME
               FROM ItineraryEvent;
         """
      ).fetchall()
   }

   assert events[ ItineraryEventType.ARRIVAL.value ] == ( '9:30 AM', '9:30 AM' )
   assert events[ ItineraryEventType.LUNCH.value ] == ( '12:10 PM', '12:40 PM' )
   assert events[ ItineraryEventType.DEPARTURE.value ] == ( '5:00 PM', '5:00 PM' )


def Test_ShiftItemsAfterUnschedule_TestWildEncounterOccupied_ExpectNoShift(
      shift_applier_conn: sqlite3.Connection ) -> None:
   shift_applier_conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, NULL, ?, ? );
      """,
      ( 'Cheetah', 'Africa Savanna', '1:00 PM', '1:08 PM' ) )
   shift_applier_conn.execute(
      """   INSERT INTO ItineraryWildEncounter (
               WILD_ENCOUNTER,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES ( ?, ?, ?, 0 );
      """,
      ( 'African Rainforest', '12:30 PM', '1:00 PM' ) )
   shift_applier_conn.commit()
   cur = shift_applier_conn.cursor()

   GuestScheduleShiftApplier.shift_items_after_unschedule(
      shift_applier_conn,
      cur,
      anchor_end_seconds=13 * 3600,
      shift_seconds=-20 * 60,
      freed_block=TimeBlock(
         start_seconds=12 * 3600 + 40 * 60,
         end_seconds=13 * 3600,
      ) )
   shift_applier_conn.commit()
   cur.close()

   cheetah = shift_applier_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ? AND EXHIBIT = ?;
      """,
      ( 'Cheetah', 'Africa Savanna' ),
   ).fetchone()

   assert cheetah is not None
   assert cheetah[ 'START_TIME' ] == '1:00 PM'
   assert cheetah[ 'END_TIME' ] == '1:08 PM'


def Test_ShiftItemsAfterUnschedule_TestCoveredByTalk_ExpectNotShifted(
      shift_applier_conn: sqlite3.Connection ) -> None:
   shift_applier_conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               COVERED_BY_TALK,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, NULL, 1, ?, ? );
      """,
      ( 'African Lion', 'Africa Savanna', '11:30 AM', '11:38 AM' ) )
   shift_applier_conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               COVERED_BY_TALK,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, NULL, 0, ?, ? );
      """,
      ( 'Cheetah', 'Africa Savanna', '11:40 AM', '11:48 AM' ) )
   shift_applier_conn.commit()
   cur = shift_applier_conn.cursor()

   GuestScheduleShiftApplier.shift_items_after_unschedule(
      shift_applier_conn,
      cur,
      anchor_end_seconds=11 * 3600 + 30 * 60,
      shift_seconds=-10 * 60 )
   shift_applier_conn.commit()
   cur.close()

   lion = shift_applier_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ? AND EXHIBIT = ?;
      """,
      ( 'African Lion', 'Africa Savanna' ),
   ).fetchone()
   cheetah = shift_applier_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ? AND EXHIBIT = ?;
      """,
      ( 'Cheetah', 'Africa Savanna' ),
   ).fetchone()

   assert lion is not None
   assert lion[ 'START_TIME' ] == '11:30 AM'
   assert lion[ 'END_TIME' ] == '11:38 AM'
   assert cheetah is not None
   assert cheetah[ 'START_TIME' ] == '11:30 AM'
   assert cheetah[ 'END_TIME' ] == '11:38 AM'


def Test_ShiftedScheduleTimes_TestInvalidSourceTimes_ExpectNone() -> None:
   assert GuestScheduleShiftApplier.shifted_schedule_times( None, None, -60 ) is None


def Test_CollectFixedActivityBlocks_TestDeletedRows_ExpectSkipped(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_guardians_talk_rows',
      lambda conn: [
         ItineraryGuardiansTalkRecord(
            talk_name='Deleted Talk',
            start_time='10:00 AM',
            end_time='10:30 AM',
            is_deleted=True ),
         ItineraryGuardiansTalkRecord(
            talk_name='Live Talk',
            start_time='11:00 AM',
            end_time='11:30 AM',
            is_deleted=False ),
      ] )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_wild_encounter_rows',
      lambda conn: [
         ItineraryWildEncounterRecord(
            wild_encounter='Deleted Encounter',
            start_time='1:00 PM',
            end_time='1:20 PM',
            is_deleted=True ),
         ItineraryWildEncounterRecord(
            wild_encounter='Live Encounter',
            start_time='2:00 PM',
            end_time='2:20 PM',
            is_deleted=False ),
      ] )

   blocks = GuestScheduleShiftApplier._collect_fixed_activity_blocks(
      object(),
      freed_block=None )

   assert blocks == [
      TimeBlock( start_seconds=11 * 3600, end_seconds=11 * 3600 + 30 * 60 ),
      TimeBlock( start_seconds=14 * 3600, end_seconds=14 * 3600 + 20 * 60 ),
   ]


def Test_ShiftedBlockOverlapsOccupied_TestInvalidShift_ExpectTrue() -> None:
   assert GuestScheduleShiftApplier._shifted_block_overlaps_occupied(
      '10:00 AM',
      '10:15 AM',
      -11 * 3600,
      [] )


def Test_GuestShiftWouldOverlapFixedActivity_TestAttractionOverlap_ExpectTrue(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_animal_rows',
      lambda conn: [] )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_attraction_rows',
      lambda conn: [
         ItineraryAttractionRecord(
            attraction='Conservation Carousel',
            old_likelihood=None,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:15 AM' ),
      ] )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_transportation_rows',
      lambda conn: [] )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_event_rows',
      lambda conn: [] )

   occupied = [
      TimeBlock( start_seconds=10 * 3600 + 45 * 60, end_seconds=11 * 3600 ),
   ]

   assert GuestScheduleShiftApplier._guest_shift_would_overlap_fixed_activity(
      object(),
      anchor_end_time='10:30 AM',
      delta_seconds=-15 * 60,
      occupied_blocks=occupied )


def Test_GuestShiftWouldOverlapFixedActivity_TestTransportationOverlap_ExpectTrue(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_animal_rows',
      lambda conn: [] )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_attraction_rows',
      lambda conn: [] )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_transportation_rows',
      lambda conn: [
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=False,
            start_time='11:00 AM',
            end_time='11:30 AM' ),
      ] )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_event_rows',
      lambda conn: [] )

   occupied = [
      TimeBlock( start_seconds=10 * 3600 + 45 * 60, end_seconds=11 * 3600 ),
   ]

   assert GuestScheduleShiftApplier._guest_shift_would_overlap_fixed_activity(
      object(),
      anchor_end_time='10:30 AM',
      delta_seconds=-15 * 60,
      occupied_blocks=occupied )


def Test_GuestShiftWouldOverlapFixedActivity_TestEventOverlap_ExpectTrue(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_animal_rows',
      lambda conn: [] )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_attraction_rows',
      lambda conn: [] )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_transportation_rows',
      lambda conn: [] )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_event_rows',
      lambda conn: [
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time='11:00 AM',
            end_time='11:30 AM' ),
      ] )

   occupied = [
      TimeBlock( start_seconds=10 * 3600 + 45 * 60, end_seconds=11 * 3600 ),
   ]

   assert GuestScheduleShiftApplier._guest_shift_would_overlap_fixed_activity(
      object(),
      anchor_end_time='10:30 AM',
      delta_seconds=-15 * 60,
      occupied_blocks=occupied )


def Test_ShiftGuestScheduledAnimalRows_TestInvalidShiftTimes_ExpectSkip(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   update_calls: list[ str ] = []

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_animal_rows',
      lambda conn: [
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='11:00 AM',
            end_time='11:08 AM' ),
      ] )
   monkeypatch.setattr(
      GuestScheduleShiftApplier,
      'shifted_schedule_times',
      lambda start_time, end_time, delta_seconds: None )
   monkeypatch.setattr(
      ScheduleItineraryItemProvider,
      'update_itinerary_animal_schedule',
      lambda *args, **kwargs: update_calls.append( 'updated' ) )

   GuestScheduleShiftApplier._shift_guest_scheduled_animal_rows(
      object(),
      object(),
      anchor_end_time='10:30 AM',
      delta_seconds=-15 * 60 )

   assert update_calls == []


def Test_ShiftGuestScheduledAttractionRows_TestBeforeAnchor_ExpectSkip(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   update_calls: list[ str ] = []

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_attraction_rows',
      lambda conn: [
         ItineraryAttractionRecord(
            attraction='Conservation Carousel',
            old_likelihood=None,
            new_likelihood=100,
            start_time='9:00 AM',
            end_time='9:15 AM' ),
         ItineraryAttractionRecord(
            attraction='Kids Zoo',
            old_likelihood=None,
            new_likelihood=100,
            start_time=None,
            end_time=None ),
      ] )
   monkeypatch.setattr(
      ScheduleItineraryItemProvider,
      'update_itinerary_attraction_schedule',
      lambda *args, **kwargs: update_calls.append( 'updated' ) )

   GuestScheduleShiftApplier._shift_guest_scheduled_attraction_rows(
      object(),
      object(),
      anchor_end_time='10:30 AM',
      delta_seconds=-15 * 60 )

   assert update_calls == []


def Test_ShiftGuestScheduledTransportationRows_TestNoRouteOrBadLeg_ExpectSkip(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   update_calls: list[ str ] = []
   call_count = { 'n': 0 }

   def _shifted(
         start_time: str | None,
         end_time: str | None,
         delta_seconds: int,
      ) -> tuple[ str, str ] | None:
      call_count[ 'n' ] += 1

      if call_count[ 'n' ] == 1:
         return ( '11:45 AM', '12:15 PM' )

      return None

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_transportation_rows',
      lambda conn: [
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=False,
            start_time='11:00 AM',
            end_time='11:30 AM',
            route=None ),
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=True,
            start_time='12:00 PM',
            end_time='12:30 PM',
            route='summer',
            legs=[
               ItineraryTransportationLeg(
                  from_station='A',
                  to_station='B',
                  start_time='12:00 PM',
                  end_time='12:30 PM',
                  transportation='Zoomobile',
                  added_as_attraction=True ),
            ] ),
      ] )
   monkeypatch.setattr( GuestScheduleShiftApplier, 'shifted_schedule_times', _shifted )
   monkeypatch.setattr(
      ItineraryTransportationProvider,
      'delete_itinerary_transportation_legs',
      lambda *args, **kwargs: update_calls.append( 'delete' ) )
   monkeypatch.setattr(
      ItineraryTransportationProvider,
      'insert_itinerary_transportation_legs',
      lambda *args, **kwargs: update_calls.append( 'insert' ) )
   monkeypatch.setattr(
      ScheduleItineraryTransportationProvider,
      'update_itinerary_transportation_schedule',
      lambda *args, **kwargs: update_calls.append( 'update' ) )

   GuestScheduleShiftApplier._shift_guest_scheduled_transportation_rows(
      object(),
      object(),
      anchor_end_time='10:30 AM',
      delta_seconds=-15 * 60 )

   assert update_calls == []


def Test_ShiftGuestScheduledEventRows_TestInvalidShift_ExpectSkip(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   update_calls: list[ str ] = []

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_event_rows',
      lambda conn: [
         ItineraryEventRecord(
            event_type=ItineraryEventType.ARRIVAL,
            start_time='9:00 AM',
            end_time='9:15 AM' ),
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time='11:00 AM',
            end_time='11:30 AM' ),
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time=None,
            end_time=None ),
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time='9:00 AM',
            end_time='9:30 AM' ),
      ] )
   monkeypatch.setattr(
      GuestScheduleShiftApplier,
      'shifted_schedule_times',
      lambda start_time, end_time, delta_seconds: None )
   monkeypatch.setattr(
      ScheduleItineraryItemProvider,
      'update_itinerary_event_schedule',
      lambda *args, **kwargs: update_calls.append( 'updated' ) )

   GuestScheduleShiftApplier._shift_guest_scheduled_event_rows(
      object(),
      object(),
      anchor_end_time='10:30 AM',
      delta_seconds=-15 * 60 )

   assert update_calls == []


def Test_ShiftedBlockOverlapsOccupied_TestUnparseableShiftedTimes_ExpectTrue(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GuestScheduleShiftApplier,
      'shifted_schedule_times',
      lambda start_time, end_time, delta_seconds: ( 'bad', 'bad' ) )
   monkeypatch.setattr(
      TimeBlockBuilder,
      'from_schedule_times',
      lambda start_time, end_time: None )

   assert GuestScheduleShiftApplier._shifted_block_overlaps_occupied(
      '11:00 AM',
      '11:30 AM',
      -15 * 60,
      [] ) is True


def Test_GuestShiftWouldOverlapFixedActivity_TestUnscheduledAndBeforeAnchor_ExpectFalse(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_animal_rows',
      lambda conn: [
         ItineraryAnimalRecord(
            species='Cheetah',
            exhibit='Africa Savanna',
            start_time=None,
            end_time=None ),
         ItineraryAnimalRecord(
            species='Lion',
            exhibit='Africa Savanna',
            start_time='9:00 AM',
            end_time='9:30 AM' ),
      ] )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_attraction_rows',
      lambda conn: [
         ItineraryAttractionRecord(
            attraction='Splash',
            old_likelihood=None,
            new_likelihood=1,
            start_time=None,
            end_time=None ),
         ItineraryAttractionRecord(
            attraction='Carousel',
            old_likelihood=None,
            new_likelihood=1,
            start_time='9:00 AM',
            end_time='9:30 AM' ),
      ] )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_transportation_rows',
      lambda conn: [
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=1,
            added_as_attraction=True,
            start_time=None,
            end_time=None ),
      ] )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_event_rows',
      lambda conn: [
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time=None,
            end_time=None ),
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time='9:00 AM',
            end_time='9:30 AM' ),
      ] )

   assert GuestScheduleShiftApplier._guest_shift_would_overlap_fixed_activity(
      object(),
      anchor_end_time='10:30 AM',
      delta_seconds=-15 * 60,
      occupied_blocks=[] ) is False


def Test_ShiftGuestScheduledAttractionRows_TestInvalidShiftTimes_ExpectSkip(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   update_calls: list[ str ] = []

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_attraction_rows',
      lambda conn: [
         ItineraryAttractionRecord(
            attraction='Splash',
            old_likelihood=None,
            new_likelihood=1,
            start_time='11:00 AM',
            end_time='11:30 AM' ),
      ] )
   monkeypatch.setattr(
      GuestScheduleShiftApplier,
      'shifted_schedule_times',
      lambda start_time, end_time, delta_seconds: None )
   monkeypatch.setattr(
      ScheduleItineraryItemProvider,
      'update_itinerary_attraction_schedule',
      lambda *args, **kwargs: update_calls.append( 'updated' ) )

   GuestScheduleShiftApplier._shift_guest_scheduled_attraction_rows(
      object(),
      object(),
      anchor_end_time='10:30 AM',
      delta_seconds=-15 * 60 )

   assert update_calls == []


def Test_ShiftGuestScheduledAnimalRows_TestUnscheduled_ExpectSkip(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   update_calls: list[ str ] = []

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_animal_rows',
      lambda conn: [
         ItineraryAnimalRecord(
            species='Cheetah',
            exhibit='Africa Savanna',
            start_time=None,
            end_time=None ),
      ] )
   monkeypatch.setattr(
      ScheduleItineraryItemProvider,
      'update_itinerary_animal_schedule',
      lambda *args, **kwargs: update_calls.append( 'updated' ) )

   GuestScheduleShiftApplier._shift_guest_scheduled_animal_rows(
      object(),
      object(),
      anchor_end_time='10:30 AM',
      delta_seconds=-15 * 60 )

   assert update_calls == []


def Test_ShiftGuestScheduledTransportationRows_TestUnscheduled_ExpectSkip(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   update_calls: list[ str ] = []

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_transportation_rows',
      lambda conn: [
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=1,
            added_as_attraction=True,
            start_time=None,
            end_time=None,
            route='summer' ),
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=1,
            added_as_attraction=True,
            start_time='12:00 PM',
            end_time='12:30 PM',
            route='summer',
            legs=[] ),
      ] )
   monkeypatch.setattr(
      GuestScheduleShiftApplier,
      'shifted_schedule_times',
      lambda start_time, end_time, delta_seconds: None )
   monkeypatch.setattr(
      ScheduleItineraryTransportationProvider,
      'update_itinerary_transportation_schedule',
      lambda *args, **kwargs: update_calls.append( 'update' ) )

   GuestScheduleShiftApplier._shift_guest_scheduled_transportation_rows(
      object(),
      object(),
      anchor_end_time='10:30 AM',
      delta_seconds=-15 * 60 )

   assert update_calls == []
