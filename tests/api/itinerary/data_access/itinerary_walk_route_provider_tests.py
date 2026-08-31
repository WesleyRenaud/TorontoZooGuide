from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_walk_route_matcher import ItineraryWalkRouteMatcher
from api.itinerary.data_access.itinerary_walk_route_provider import ItineraryWalkRouteProvider
from api.itinerary.routing.itinerary_walk_route import ItineraryWalkRoute
from api.itinerary.routing.itinerary_walk_route_builder import ItineraryWalkRouteBuilder
from api.itinerary.routing.itinerary_walk_route_stop import ItineraryWalkRouteStop
from api.itinerary.routing.walk_route_leg import WalkRouteLeg
from api.itinerary.routing.walk_route_point import WalkRoutePoint
from api.shared.enums import ScheduleItemKind


SAMPLE_ROUTE = ItineraryWalkRoute(
   stops=[
      ItineraryWalkRouteStop(
         schedule_item_kind=ScheduleItemKind.ENTRANCE,
         item_key='entrance',
         walk_node_id='n-1' ),
      ItineraryWalkRouteStop(
         schedule_item_kind=ScheduleItemKind.ANIMAL,
         item_key='African Lion||Africa Savanna||Outdoor',
         walk_node_id='n-2',
         start_time='10:00 AM',
         end_time='10:30 AM' ),
   ],
   legs=[
      WalkRouteLeg(
         from_item_key='entrance',
         to_item_key='African Lion||Africa Savanna||Outdoor',
         from_schedule_item_kind=ScheduleItemKind.ENTRANCE,
         to_schedule_item_kind=ScheduleItemKind.ANIMAL,
         node_ids=[ 'n-1', 'n-2' ],
         travel_time_minutes=5 ),
   ],
   points=[
      WalkRoutePoint(
         node_id='n-1',
         x=0.0,
         y=0.0,
         x_px=0.0,
         y_px=0.0 ),
      WalkRoutePoint(
         node_id='n-2',
         x=10.0,
         y=10.0,
         x_px=10.0,
         y_px=10.0 ),
   ] )


WALK_ROUTE_SCHEMA = """
CREATE TABLE ItineraryWalkRouteStop (
   STOP_SEQUENCE          INTEGER     NOT NULL,
   SCHEDULE_ITEM_KIND     TEXT        NOT NULL,
   ITEM_KEY               TEXT        NOT NULL,
   WALK_NODE_ID           TEXT        NOT NULL,
   START_TIME             TEXT,
   END_TIME               TEXT,
   PRIMARY KEY ( STOP_SEQUENCE )
);

CREATE TABLE ItineraryWalkRoutePoint (
   POINT_SEQUENCE         INTEGER     NOT NULL,
   WALK_NODE_ID           TEXT        NOT NULL,
   X                      REAL        NOT NULL,
   Y                      REAL        NOT NULL,
   X_PX                   REAL        NOT NULL,
   Y_PX                   REAL        NOT NULL,
   PRIMARY KEY ( POINT_SEQUENCE )
);

CREATE TABLE ItineraryWalkRouteLeg (
   LEG_SEQUENCE               INTEGER     NOT NULL,
   FROM_ITEM_KEY              TEXT        NOT NULL,
   TO_ITEM_KEY                TEXT        NOT NULL,
   FROM_SCHEDULE_ITEM_KIND    TEXT        NOT NULL,
   TO_SCHEDULE_ITEM_KIND      TEXT        NOT NULL,
   FROM_POINT_SEQUENCE        INTEGER     NOT NULL,
   TO_POINT_SEQUENCE          INTEGER     NOT NULL,
   TRAVEL_TIME_MINUTES        INTEGER     NOT NULL DEFAULT 0,
   PRIMARY KEY ( LEG_SEQUENCE )
);
"""


@pytest.fixture
def walk_route_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( WALK_ROUTE_SCHEMA )

   yield conn

   conn.close()


def Test_FetchItineraryWalkRoute_TestNoLegRows_ExpectEmpty(
      walk_route_conn: sqlite3.Connection ) -> None:
   assert ItineraryWalkRouteProvider.fetch_itinerary_walk_route(
      walk_route_conn ) == ItineraryWalkRouteBuilder.empty()


def Test_SaveItineraryWalkRoute_TestRoute_ExpectRoundTrip(
      walk_route_conn: sqlite3.Connection ) -> None:
   assert ItineraryWalkRouteProvider.save_itinerary_walk_route(
      walk_route_conn,
      SAMPLE_ROUTE )

   persisted_route = ItineraryWalkRouteProvider.fetch_itinerary_walk_route(
      walk_route_conn )

   assert ItineraryWalkRouteMatcher.matches( SAMPLE_ROUTE, persisted_route )


def Test_SaveItineraryWalkRoute_TestEmptyRoute_ExpectClearedTables(
      walk_route_conn: sqlite3.Connection ) -> None:
   assert ItineraryWalkRouteProvider.save_itinerary_walk_route(
      walk_route_conn,
      SAMPLE_ROUTE )
   assert ItineraryWalkRouteProvider.save_itinerary_walk_route(
      walk_route_conn,
      ItineraryWalkRouteBuilder.empty() )

   assert ItineraryWalkRouteProvider.fetch_itinerary_walk_route(
      walk_route_conn ) == ItineraryWalkRouteBuilder.empty()
