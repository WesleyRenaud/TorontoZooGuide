from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.scheduling.core.time_block import TimeBlock
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
