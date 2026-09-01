from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.operations.itinerary_item_unscheduler import ItineraryItemUnscheduler
from api.itinerary.transportation_schedule_item_key import TransportationScheduleItemKey
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.enums import ItineraryEventType


UNSCHEDULER_SCHEMA = """
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

CREATE TABLE ItineraryEvent (
   EVENT_TYPE           TEXT        NOT NULL PRIMARY KEY,
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
"""

CAROUSEL = 'Conservation Carousel'
ZOOMOBILE = 'Zoomobile'
ZOOMOBILE_ATTRACTION_START = '11:00 AM'
ZOOMOBILE_ATTRACTION_END = '11:30 AM'
ZOOMOBILE_TRANSIT_START = '11:30 AM'
ZOOMOBILE_TRANSIT_END = '12:00 PM'
ZOOMOBILE_TRANSIT_ROUTE = 'zoomobile-route'
LION_KEY = AnimalScheduleItemKey(
   species='African Lion',
   exhibit='Africa Savanna',
)


@pytest.fixture
def unscheduler_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( UNSCHEDULER_SCHEMA )
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
      ( 'African Lion', 'Africa Savanna', '10:00 AM', '10:08 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( CAROUSEL, '11:00 AM', '11:20 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ? );
      """,
      ( ItineraryEventType.LUNCH.value, '12:00 PM', '12:40 PM' ) )
   conn.commit()

   yield conn

   conn.close()


def _insert_zoomobile_transportation_rows( conn: sqlite3.Connection ) -> None:
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


def _zoomobile_saved_itinerary() -> SavedItinerary:
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


@pytest.fixture
def zoomobile_unscheduler_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( UNSCHEDULER_SCHEMA )
   _insert_zoomobile_transportation_rows( conn )

   yield conn

   conn.close()


def _fetch_transportation_row(
      conn: sqlite3.Connection,
      *,
      added_as_attraction: bool ) -> sqlite3.Row:
   row = conn.execute(
      """   SELECT
               START_TIME,
               END_TIME,
               ROUTE,
               BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = ?;
      """,
      ( ZOOMOBILE, added_as_attraction ),
   ).fetchone()

   assert row is not None
   return row


def _fetch_transit_legs( conn: sqlite3.Connection ) -> list[ tuple[ str, str, str, str ] ]:
   rows = conn.execute(
      """   SELECT FROM_STATION, TO_STATION, START_TIME, END_TIME
            FROM ItineraryTransportationLeg
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 0
            ORDER BY START_TIME;
      """,
      ( ZOOMOBILE, ),
   ).fetchall()

   return [
      (
         row[ 'FROM_STATION' ],
         row[ 'TO_STATION' ],
         row[ 'START_TIME' ],
         row[ 'END_TIME' ],
      )
      for row in rows
   ]


def Test_Apply_TestAnimalKey_ExpectClearedSchedule(
      unscheduler_conn: sqlite3.Connection ) -> None:
   cur = unscheduler_conn.cursor()
   ItineraryItemUnscheduler.apply( cur, LION_KEY )
   unscheduler_conn.commit()
   cur.close()

   row = unscheduler_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAnimal
            WHERE SPECIES = ?
              AND EXHIBIT = ?;
      """,
      ( 'African Lion', 'Africa Savanna' ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] is None
   assert row[ 'END_TIME' ] is None


def Test_Apply_TestAttractionKey_ExpectClearedSchedule(
      unscheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_unscheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-15',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
      ) )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_unscheduler.SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row',
      lambda saved_itinerary, schedule_item_key: None )

   cur = unscheduler_conn.cursor()
   ItineraryItemUnscheduler.apply(
      cur,
      AttractionScheduleItemKey( name=CAROUSEL ) )
   unscheduler_conn.commit()
   cur.close()

   row = unscheduler_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryAttraction
            WHERE ATTRACTION = ?;
      """,
      ( CAROUSEL, ),
   ).fetchone()

   assert row is not None
   assert row[ 'START_TIME' ] is None
   assert row[ 'END_TIME' ] is None


def Test_Apply_TestEventType_ExpectDeletedRow(
      unscheduler_conn: sqlite3.Connection ) -> None:
   cur = unscheduler_conn.cursor()
   ItineraryItemUnscheduler.apply( cur, ItineraryEventType.LUNCH )
   unscheduler_conn.commit()
   cur.close()

   count = unscheduler_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryEvent;' ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0


def Test_Apply_TestAttractionZoomobileKey_ExpectAttractionModeClearedTransitPreserved(
      zoomobile_unscheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_unscheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: _zoomobile_saved_itinerary() )
   transit_legs_before = _fetch_transit_legs( zoomobile_unscheduler_conn )

   cur = zoomobile_unscheduler_conn.cursor()
   ItineraryItemUnscheduler.apply(
      cur,
      AttractionScheduleItemKey( name=ZOOMOBILE ) )
   zoomobile_unscheduler_conn.commit()
   cur.close()

   attraction_row = _fetch_transportation_row(
      zoomobile_unscheduler_conn,
      added_as_attraction=True )
   transit_row = _fetch_transportation_row(
      zoomobile_unscheduler_conn,
      added_as_attraction=False )

   assert attraction_row[ 'START_TIME' ] is None
   assert attraction_row[ 'END_TIME' ] is None
   assert transit_row[ 'START_TIME' ] == ZOOMOBILE_TRANSIT_START
   assert transit_row[ 'END_TIME' ] == ZOOMOBILE_TRANSIT_END
   assert transit_row[ 'ROUTE' ] == ZOOMOBILE_TRANSIT_ROUTE
   assert transit_row[ 'BULK_TRANSIT_EVALUATED' ] == 1
   assert _fetch_transit_legs( zoomobile_unscheduler_conn ) == transit_legs_before


def Test_Apply_TestTransportationAttractionModeKey_ExpectAttractionModeClearedTransitPreserved(
      zoomobile_unscheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_unscheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: _zoomobile_saved_itinerary() )
   transit_legs_before = _fetch_transit_legs( zoomobile_unscheduler_conn )

   cur = zoomobile_unscheduler_conn.cursor()
   ItineraryItemUnscheduler.apply(
      cur,
      TransportationScheduleItemKey(
         name=ZOOMOBILE,
         added_as_attraction=True ) )
   zoomobile_unscheduler_conn.commit()
   cur.close()

   attraction_row = _fetch_transportation_row(
      zoomobile_unscheduler_conn,
      added_as_attraction=True )
   transit_row = _fetch_transportation_row(
      zoomobile_unscheduler_conn,
      added_as_attraction=False )

   assert attraction_row[ 'START_TIME' ] is None
   assert attraction_row[ 'END_TIME' ] is None
   assert transit_row[ 'START_TIME' ] == ZOOMOBILE_TRANSIT_START
   assert transit_row[ 'END_TIME' ] == ZOOMOBILE_TRANSIT_END
   assert transit_row[ 'ROUTE' ] == ZOOMOBILE_TRANSIT_ROUTE
   assert transit_row[ 'BULK_TRANSIT_EVALUATED' ] == 1
   assert _fetch_transit_legs( zoomobile_unscheduler_conn ) == transit_legs_before
