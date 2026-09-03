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

PENGUIN_KEY = AnimalScheduleItemKey(
   species='African Penguin',
   exhibit='Africa Savanna',
)

CAROUSEL_KEY = AttractionScheduleItemKey( name='Conservation Carousel' )

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


def Test_Apply_TestMissingAnimalInsertIfMissing_ExpectInserted(
      target_conn: sqlite3.Connection ) -> None:
   inserted = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      PENGUIN_KEY,
      '11:00 AM',
      '11:08 AM',
      insert_if_missing=True )

   assert inserted

   row = target_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( 'African Penguin', 'Africa Savanna' ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] == '11:00 AM'
   assert row[ 'END_TIME' ] == '11:08 AM'


def Test_Apply_TestExistingAnimalInsertIfMissing_ExpectUpdated(
      target_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ScheduleItineraryItemProvider,
      'insert_itinerary_animal_schedule',
      lambda *_args, **_kwargs: False )

   updated = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      LION_KEY,
      '11:30 AM',
      '11:38 AM',
      insert_if_missing=True )

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
   assert row[ 'START_TIME' ] == '11:30 AM'
   assert row[ 'END_TIME' ] == '11:38 AM'


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

   inserted = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      CAROUSEL_KEY,
      '12:00 PM',
      '12:12 PM',
      insert_if_missing=True )

   assert inserted

   row = target_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( 'Conservation Carousel', ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] == '12:00 PM'
   assert row[ 'END_TIME' ] == '12:12 PM'


def Test_Apply_TestExistingAttraction_ExpectUpdated(
      target_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   target_conn.execute(
      """   INSERT INTO ItineraryAttraction ( ATTRACTION, START_TIME, END_TIME )
            VALUES ( ?, ?, ? );
      """,
      ( 'Conservation Carousel', '9:00 AM', '9:12 AM' ) )
   target_conn.commit()

   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda _conn: object() )
   monkeypatch.setattr(
      SavedItineraryScheduleItemRowFinder,
      'find_saved_itinerary_schedule_item_row',
      lambda _saved, _key: None )

   updated = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      CAROUSEL_KEY,
      '1:00 PM',
      '1:12 PM',
      insert_if_missing=False )

   assert updated

   row = target_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( 'Conservation Carousel', ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] == '1:00 PM'
   assert row[ 'END_TIME' ] == '1:12 PM'


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

   assert ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      ZOOMOBILE_KEY,
      '10:00 AM',
      '10:20 AM',
      insert_if_missing=False ) is True
   assert captured[ 'args' ] == (
      'Zoomobile',
      True,
      '10:00 AM',
      'summer',
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

   assert ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      ZOOMOBILE_KEY,
      '10:00 AM',
      '10:20 AM',
      insert_if_missing=False ) is False


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

   assert ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      ZOOMOBILE_KEY,
      '10:00 AM',
      '10:20 AM',
      insert_if_missing=False ) is False


def Test_Apply_TestAttractionInsertIfMissingAlreadyPresent_ExpectUpdated(
      target_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   target_conn.execute(
      """   INSERT INTO ItineraryAttraction ( ATTRACTION, START_TIME, END_TIME )
            VALUES ( ?, ?, ? );
      """,
      ( 'Conservation Carousel', '9:00 AM', '9:12 AM' ) )
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

   updated = ListedScheduleTargetResolver.apply(
      target_conn.cursor(),
      CAROUSEL_KEY,
      '2:00 PM',
      '2:12 PM',
      insert_if_missing=True )

   assert updated

   row = target_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( 'Conservation Carousel', ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] == '2:00 PM'
   assert row[ 'END_TIME' ] == '2:12 PM'
