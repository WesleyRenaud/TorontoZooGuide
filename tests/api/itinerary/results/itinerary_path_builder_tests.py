from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_walk_route_provider import ItineraryWalkRouteProvider
from api.itinerary.results.itinerary_path_builder import ItineraryPathBuilder
from api.itinerary.routing.itinerary_walk_route import ItineraryWalkRoute
from api.itinerary.routing.itinerary_walk_route_stop import ItineraryWalkRouteStop
from api.itinerary.routing.walk_route_leg import WalkRouteLeg
from api.itinerary.routing.walk_route_point import WalkRoutePoint
from api.shared.enums import ScheduleItemKind


EMPTY_ITINERARY_PATH = {
   'stops': [],
   'legs': [],
   'points': [],
}

SAVED_ITINERARY_PATH = {
   'stops': [
      {
         'schedule_item_kind': ScheduleItemKind.ENTRANCE.value,
         'item_key': 'entrance',
         'walk_node_id': 'n-1',
         'start_time': None,
         'end_time': None,
      },
      {
         'schedule_item_kind': ScheduleItemKind.ANIMAL.value,
         'item_key': 'African Lion||Africa Savanna||Outdoor',
         'walk_node_id': 'n-2',
         'start_time': '10:00 AM',
         'end_time': '10:30 AM',
      },
   ],
   'legs': [
      {
         'from_item_key': 'entrance',
         'to_item_key': 'African Lion||Africa Savanna||Outdoor',
         'from_schedule_item_kind': ScheduleItemKind.ENTRANCE.value,
         'to_schedule_item_kind': ScheduleItemKind.ANIMAL.value,
         'node_ids': [ 'n-1', 'n-2' ],
         'travel_time_minutes': 5,
      },
   ],
   'points': [
      {
         'node_id': 'n-1',
         'x': 0.0,
         'y': 0.0,
         'x_px': 0.0,
         'y_px': 0.0,
      },
      {
         'node_id': 'n-2',
         'x': 10.0,
         'y': 10.0,
         'x_px': 10.0,
         'y_px': 10.0,
      },
   ],
}

SAVED_ROUTE = ItineraryWalkRoute(
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


def Test_Build_TestNoConnection_ExpectEmptyPath() -> None:
   assert ItineraryPathBuilder.build( None ) == EMPTY_ITINERARY_PATH


def Test_Build_TestConnection_ExpectFetchedRoute(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   conn = sqlite3.connect( ':memory:' )
   monkeypatch.setattr(
      ItineraryWalkRouteProvider,
      'fetch_itinerary_walk_route',
      lambda connection: SAVED_ROUTE )

   assert ItineraryPathBuilder.build( conn ) == SAVED_ITINERARY_PATH
