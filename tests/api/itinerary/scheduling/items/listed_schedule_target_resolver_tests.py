from __future__ import annotations

from datetime import date
import sqlite3
from typing import Any

import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.saved_itinerary_schedule_item_row_finder import SavedItineraryScheduleItemRowFinder
from api.itinerary.data_access.schedule_itinerary_item_provider import ScheduleItineraryItemProvider
from api.itinerary.data_access.schedule_itinerary_transportation_provider import ScheduleItineraryTransportationProvider
from api.itinerary.scheduling.items.listed_schedule_target_resolver import ListedScheduleTargetResolver
from api.itinerary.transportation.transportation_day_loop import TransportationDayLoop
from api.itinerary.transportation.transportation_day_loop_fetcher import TransportationDayLoopFetcher
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.shared.calendar_dates import DateValues
from api.shared.duration_values import DurationValues
from api.shared.enums.position import Position

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
   OLD_LIKELIHOOD                       INTEGER,
   NEW_LIKELIHOOD                       INTEGER,
   IS_ADDED                             INTEGER     NOT NULL DEFAULT 0,
   ADDED_BY_TRANSPORTATION              INTEGER     NOT NULL DEFAULT 0,
   START_TIME                           TEXT,
   END_TIME                             TEXT
);

CREATE TABLE ItineraryAttraction (
   ATTRACTION                           TEXT        NOT NULL PRIMARY KEY,
   OLD_LIKELIHOOD                       INTEGER,
   NEW_LIKELIHOOD                       INTEGER,
   START_TIME                           TEXT,
   END_TIME                             TEXT
);
"""

LION_KEY = AnimalScheduleItemKey(
   species='African Lion',
   exhibit='Africa Savanna',
)
LION_DURATION_MINUTES = 8

PENGUIN_KEY = AnimalScheduleItemKey(
   species='African Penguin',
   exhibit='Africa Savanna',
)
PENGUIN_DURATION_MINUTES = 8

CAROUSEL_KEY = AttractionScheduleItemKey( name='Conservation Carousel' )
CAROUSEL_DURATION_MINUTES = 12

ZOOMOBILE_KEY = AttractionScheduleItemKey( name='Zoomobile' )

DAY_LOOP = TransportationDayLoop(
   transportation='Zoomobile',
   route='summer',
   main_station='Main Zoomobile Station',
   legs=[
      TransportationRouteLegSegment(
         'Main Zoomobile Station',
         'Canadian Domain Zoomobile Station',
         20 ),
   ],
)

TRANSPORTATION_ROW = ItineraryTransportationRecord(
   transportation='Zoomobile',
   old_likelihood=None,
   new_likelihood=100,
   added_as_attraction=True,
)


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
      ( LION_KEY.species, LION_KEY.exhibit, LION_DURATION_MINUTES ) )
   conn.execute(
      """   INSERT INTO Attraction (
               NAME,
               DEFAULT_ITINERARY_DURATION_MINUTES,
               IS_ALSO_TRANSPORTATION
            )
            VALUES ( ?, ?, 0 );
      """,
      ( CAROUSEL_KEY.name, CAROUSEL_DURATION_MINUTES ) )
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
      ( LION_KEY.species, LION_KEY.exhibit ) )
   conn.commit()

   yield conn

   conn.close()


def Test_Resolve_TestAnimalDefault_ExpectEnclosureDuration(
      target_conn: sqlite3.Connection ) -> None:
   target = ListedScheduleTargetResolver.resolve( target_conn, LION_KEY )

   assert target.default_duration_seconds == DurationValues.minutes_to_seconds(
      LION_DURATION_MINUTES )


def Test_Resolve_TestAttractionDefault_ExpectAttractionDuration(
      target_conn: sqlite3.Connection ) -> None:
   target = ListedScheduleTargetResolver.resolve( target_conn, CAROUSEL_KEY )

   assert target.default_duration_seconds == DurationValues.minutes_to_seconds(
      CAROUSEL_DURATION_MINUTES )


def Test_Apply_TestExistingAnimal_ExpectScheduleUpdated(
      target_conn: sqlite3.Connection ) -> None:
   start_time = '10:00 AM'
   end_time = DateValues.add_minutes_to_time( start_time, LION_DURATION_MINUTES )

   updated = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      LION_KEY,
      start_time,
      end_time,
      insert_if_missing=False )

   assert updated

   row = target_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( LION_KEY.species, LION_KEY.exhibit ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] == start_time
   assert row[ 'END_TIME' ] == end_time


def Test_Apply_TestMissingAnimalInsertIfMissing_ExpectInserted(
      target_conn: sqlite3.Connection ) -> None:
   start_time = '11:00 AM'
   end_time = DateValues.add_minutes_to_time( start_time, PENGUIN_DURATION_MINUTES )

   inserted = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      PENGUIN_KEY,
      start_time,
      end_time,
      insert_if_missing=True )

   assert inserted

   row = target_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( PENGUIN_KEY.species, PENGUIN_KEY.exhibit ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] == start_time
   assert row[ 'END_TIME' ] == end_time


def Test_Apply_TestExistingAnimalInsertIfMissing_ExpectUpdated(
      target_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ScheduleItineraryItemProvider,
      'insert_itinerary_animal_schedule',
      lambda *_args, **_kwargs: False )

   start_time = '11:30 AM'
   end_time = DateValues.add_minutes_to_time( start_time, LION_DURATION_MINUTES )

   updated = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      LION_KEY,
      start_time,
      end_time,
      insert_if_missing=True )

   assert updated

   row = target_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( LION_KEY.species, LION_KEY.exhibit ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] == start_time
   assert row[ 'END_TIME' ] == end_time


def Test_Apply_TestAttractionInsertIfMissing_ExpectInserted(
      target_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: object() )
   monkeypatch.setattr(
      SavedItineraryScheduleItemRowFinder,
      'find_saved_itinerary_schedule_item_row',
      lambda _saved, _key: None )

   start_time = '12:00 PM'
   end_time = DateValues.add_minutes_to_time( start_time, CAROUSEL_DURATION_MINUTES )

   inserted = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      CAROUSEL_KEY,
      start_time,
      end_time,
      insert_if_missing=True )

   assert inserted

   row = target_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( CAROUSEL_KEY.name, ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] == start_time
   assert row[ 'END_TIME' ] == end_time


def Test_Apply_TestExistingAttraction_ExpectUpdated(
      target_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   target_conn.execute(
      """   INSERT INTO ItineraryAttraction ( ATTRACTION, START_TIME, END_TIME )
            VALUES ( ?, ?, ? );
      """,
      (
         CAROUSEL_KEY.name,
         '9:00 AM',
         DateValues.add_minutes_to_time( '9:00 AM', CAROUSEL_DURATION_MINUTES ) ) )
   target_conn.commit()

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: object() )
   monkeypatch.setattr(
      SavedItineraryScheduleItemRowFinder,
      'find_saved_itinerary_schedule_item_row',
      lambda _saved, _key: None )

   start_time = '1:00 PM'
   end_time = DateValues.add_minutes_to_time( start_time, CAROUSEL_DURATION_MINUTES )

   updated = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      CAROUSEL_KEY,
      start_time,
      end_time,
      insert_if_missing=False )

   assert updated

   row = target_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( CAROUSEL_KEY.name, ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] == start_time
   assert row[ 'END_TIME' ] == end_time


def Test_Apply_TestTransportationDayLoop_ExpectProviderApplied(
      target_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, Any ] = {}

   monkeypatch.setattr(
      SavedItineraryScheduleItemRowFinder,
      'find_saved_itinerary_schedule_item_row',
      lambda _saved, _key: TRANSPORTATION_ROW )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: object() )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda _conn: '2026-06-15' )
   monkeypatch.setattr(
      TransportationDayLoopFetcher,
      'fetch',
      lambda _conn, *, transportation, target_date: (
         DAY_LOOP
         if transportation == 'Zoomobile' and target_date == date( 2026, 6, 15 )
         else None ) )

   def apply_itinerary_transportation_schedule(
         _cur: sqlite3.Cursor,
         *,
         name: str,
         added_as_attraction: bool,
         start_time: str,
         route: str,
         legs: list[ TransportationRouteLegSegment ] ) -> bool:
      captured[ 'args' ] = ( name, added_as_attraction, start_time, route, legs )
      return True

   monkeypatch.setattr(
      ScheduleItineraryTransportationProvider,
      'apply_itinerary_transportation_schedule',
      apply_itinerary_transportation_schedule )

   start_time = '10:00 AM'
   end_time = DateValues.add_minutes_to_time(
      start_time,
      DAY_LOOP.legs[ Position.FIRST ].duration_minutes )

   result = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      ZOOMOBILE_KEY,
      start_time,
      end_time,
      insert_if_missing=False )

   assert result is True
   assert captured[ 'args' ] == (
      DAY_LOOP.transportation,
      TRANSPORTATION_ROW.added_as_attraction,
      start_time,
      DAY_LOOP.route,
      DAY_LOOP.legs )


def Test_Apply_TestTransportationMissingVisitDate_ExpectFalse(
      target_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      SavedItineraryScheduleItemRowFinder,
      'find_saved_itinerary_schedule_item_row',
      lambda _saved, _key: TRANSPORTATION_ROW )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: object() )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda _conn: None )

   result = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      ZOOMOBILE_KEY,
      '10:00 AM',
      '10:20 AM',
      insert_if_missing=False )

   assert result is False


def Test_Apply_TestTransportationMissingDayLoop_ExpectFalse(
      target_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      SavedItineraryScheduleItemRowFinder,
      'find_saved_itinerary_schedule_item_row',
      lambda _saved, _key: TRANSPORTATION_ROW )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: object() )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date',
      lambda _conn: '2026-06-15' )
   monkeypatch.setattr(
      TransportationDayLoopFetcher,
      'fetch',
      lambda *_args, **_kwargs: None )

   result = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      ZOOMOBILE_KEY,
      '10:00 AM',
      '10:20 AM',
      insert_if_missing=False )

   assert result is False


def Test_Apply_TestAttractionInsertIfMissingAlreadyPresent_ExpectUpdated(
      target_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   target_conn.execute(
      """   INSERT INTO ItineraryAttraction ( ATTRACTION, START_TIME, END_TIME )
            VALUES ( ?, ?, ? );
      """,
      (
         CAROUSEL_KEY.name,
         '9:00 AM',
         DateValues.add_minutes_to_time( '9:00 AM', CAROUSEL_DURATION_MINUTES ) ) )
   target_conn.commit()

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: object() )
   monkeypatch.setattr(
      SavedItineraryScheduleItemRowFinder,
      'find_saved_itinerary_schedule_item_row',
      lambda _saved, _key: None )
   monkeypatch.setattr(
      ScheduleItineraryItemProvider,
      'insert_itinerary_attraction_schedule',
      lambda *_args, **_kwargs: False )

   start_time = '2:00 PM'
   end_time = DateValues.add_minutes_to_time( start_time, CAROUSEL_DURATION_MINUTES )

   updated = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      CAROUSEL_KEY,
      start_time,
      end_time,
      insert_if_missing=True )

   assert updated

   row = target_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( CAROUSEL_KEY.name, ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] == start_time
   assert row[ 'END_TIME' ] == end_time
