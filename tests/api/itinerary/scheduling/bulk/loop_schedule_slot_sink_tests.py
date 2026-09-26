from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.scheduling.bulk.loop_schedule_slot_sink import LoopScheduleSlotSink
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.transportation.transportation_day_loop import TransportationDayLoop
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.shared.calendar_dates import DateValues
from api.shared.enums.position import Position

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
   SPECIES                 TEXT        NOT NULL,
   EXHIBIT                 TEXT        NOT NULL,
   ENCLOSURE_NAME          TEXT,
   OLD_LIKELIHOOD          INTEGER,
   NEW_LIKELIHOOD          INTEGER,
   IS_ADDED                INTEGER     NOT NULL DEFAULT 0,
   COVERED_BY_TALK         INTEGER     NOT NULL DEFAULT 0,
   ADDED_BY_TRANSPORTATION INTEGER     NOT NULL DEFAULT 0,
   START_TIME              TEXT,
   END_TIME                TEXT
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
   animal_start_time = '10:00 AM'
   attraction_start_time = '11:00 AM'
   slots = [
      ( LION, animal_start_time, '10:08 AM' ),
      ( CAROUSEL, attraction_start_time, '11:20 AM' ),
   ]

   saved = sink.save( slot_sink_conn, blockers, slots )

   assert saved is True
   assert sink.slots == slots
   assert len( blockers ) == 2
   assert blockers[ Position.FIRST ].start_seconds == DateValues.time_value_in_seconds(
      animal_start_time )
   assert blockers[ Position.SECOND ].start_seconds == DateValues.time_value_in_seconds(
      attraction_start_time )


def Test_Save_TestPersistAnimalSlot_ExpectDatabaseUpdated(
      slot_sink_conn: sqlite3.Connection ) -> None:
   sink = LoopScheduleSlotSink( persist=True )
   blockers: list[ TimeBlock ] = []
   start_time = '10:00 AM'
   end_time = '10:08 AM'

   saved = sink.save(
      slot_sink_conn,
      blockers,
      [ ( LION, start_time, end_time ) ] )

   row = slot_sink_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?;
      """,
      ( LION.species, ),
   ).fetchone()

   assert saved is True
   assert row is not None
   assert row[ 'START_TIME' ] == start_time
   assert row[ 'END_TIME' ] == end_time
   assert len( blockers ) == 1


def Test_Save_TestPersistAttractionSlot_ExpectDatabaseUpdated(
      slot_sink_conn: sqlite3.Connection ) -> None:
   sink = LoopScheduleSlotSink( persist=True )
   blockers: list[ TimeBlock ] = []
   start_time = '11:00 AM'
   end_time = '11:20 AM'

   saved = sink.save(
      slot_sink_conn,
      blockers,
      [ ( CAROUSEL, start_time, end_time ) ] )

   row = slot_sink_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( CAROUSEL.attraction, ),
   ).fetchone()

   assert saved is True
   assert row is not None
   assert row[ 'START_TIME' ] == start_time
   assert row[ 'END_TIME' ] == end_time
   assert len( blockers ) == 1


def Test_Save_TestPersistTransportationSlot_ExpectScheduleApplied(
      slot_sink_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   zoomobile = ItineraryTransportationRecord(
      transportation='Zoomobile',
      added_as_attraction=True,
      old_likelihood=None,
      new_likelihood=100 )
   day_loop = TransportationDayLoop(
      transportation='Zoomobile',
      route='summer',
      main_station='Main',
      legs=[ TransportationRouteLegSegment( 'Main', 'Africa', 10 ) ] )
   apply_calls: list[ object ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.loop_schedule_slot_sink.ItineraryProvider.fetch_itinerary_date',
      lambda conn: '2026-06-20' )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.loop_schedule_slot_sink.TransportationDayLoopFetcher.fetch',
      lambda conn, *, transportation, target_date: day_loop )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.loop_schedule_slot_sink.ScheduleItineraryTransportationProvider.apply_itinerary_transportation_schedule',
      lambda cur, *, name, added_as_attraction, start_time, route, legs: (
         apply_calls.append( ( name, start_time, route ) ) or True ) )

   sink = LoopScheduleSlotSink( persist=True )
   saved = sink.save(
      slot_sink_conn,
      [],
      [ ( zoomobile, '10:00 AM', '11:00 AM' ) ] )

   assert saved is True
   assert apply_calls == [ ( 'Zoomobile', '10:00 AM', 'summer' ) ]


def Test_Save_TestTransportationDayLoopMissing_ExpectFalse(
      slot_sink_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   zoomobile = ItineraryTransportationRecord(
      transportation='Zoomobile',
      added_as_attraction=True,
      old_likelihood=None,
      new_likelihood=100 )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.loop_schedule_slot_sink.ItineraryProvider.fetch_itinerary_date',
      lambda conn: '2026-06-20' )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.loop_schedule_slot_sink.TransportationDayLoopFetcher.fetch',
      lambda conn, *, transportation, target_date: None )

   sink = LoopScheduleSlotSink( persist=True )
   saved = sink.save(
      slot_sink_conn,
      [],
      [ ( zoomobile, '10:00 AM', '11:00 AM' ) ] )

   assert saved is False


def Test_Save_TestPersistFailure_ExpectRollbackAndFalse(
      slot_sink_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.loop_schedule_slot_sink.ScheduleItineraryItemProvider.update_itinerary_animal_schedule',
      lambda cur, *, species, exhibit, enclosure_name, start_time, end_time: False )

   sink = LoopScheduleSlotSink( persist=True )
   blockers: list[ TimeBlock ] = []
   saved = sink.save(
      slot_sink_conn,
      blockers,
      [ ( LION, '10:00 AM', '10:08 AM' ) ] )

   assert saved is False
   assert blockers == []
   row = slot_sink_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?;
      """,
      ( LION.species, ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] is None
   assert row[ 'END_TIME' ] is None
