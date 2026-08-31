from __future__ import annotations

import pytest

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.routing.itinerary_stop import ENTRANCE_ITEM_KEY
from api.itinerary.routing.itinerary_walk_route_builder import ItineraryWalkRouteBuilder
from api.models import Animal
from api.models import Itinerary
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode
from api.walk_graph.viewing_walk_node_id_resolver import ViewingWalkNodeIdResolver


VISIT_DATE = '2026-06-20'
ARRIVAL_TIME = '9:30 AM'
DEPARTURE_TIME = '5:00 PM'

ENTRANCE_NODE_ID = 'n-1'
LION_WALK_NODE_ID = 'n-2'


def _node( node_id: str, x_px: float, y_px: float ) -> WalkGraphNode:
   return {
      'id': node_id,
      'x': x_px / 100.0,
      'y': y_px / 100.0,
      'x_px': x_px,
      'y_px': y_px,
   }


TEST_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': ENTRANCE_NODE_ID,
   'nodes': [
      _node( ENTRANCE_NODE_ID, 0.0, 0.0 ),
      _node( LION_WALK_NODE_ID, 10.0, 0.0 ),
   ],
   'edges': [
      { 'from': ENTRANCE_NODE_ID, 'to': LION_WALK_NODE_ID, 'length_px': 10.0 },
      { 'from': LION_WALK_NODE_ID, 'to': ENTRANCE_NODE_ID, 'length_px': 10.0 },
   ],
}

UNSCHEDULED_LION = Animal(
   species='African Lion',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
   enclosure_type='Outdoor',
   x_coord=10.0,
   y_coord=0.0,
)

SCHEDULED_LION = Animal(
   species='African Lion',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
   enclosure_type='Outdoor',
   x_coord=10.0,
   y_coord=0.0,
   start_time='10:00 AM',
   end_time='10:30 AM',
)


def _clear_walk_graph_provider_cache() -> None:
   WalkGraphProvider.fetch.cache_clear()


@pytest.fixture
def stub_walk_graph( monkeypatch: pytest.MonkeyPatch ) -> None:
   _clear_walk_graph_provider_cache()
   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: TEST_GRAPH )
   monkeypatch.setattr(
      ViewingWalkNodeIdResolver,
      'resolve',
      lambda *args, **kwargs: LION_WALK_NODE_ID )
   yield


def _itinerary( *animals: Animal ) -> Itinerary:
   return ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=list( animals ),
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME )


def Test_Build_TestUnscheduledStopsOnly_ExpectEmptyRoute(
      stub_walk_graph: None ) -> None:
   walk_route = ItineraryWalkRouteBuilder.build(
      _itinerary( UNSCHEDULED_LION ) )

   assert walk_route == ItineraryWalkRouteBuilder.empty()


def Test_Build_TestScheduledAnimal_ExpectRoundTripRoute(
      stub_walk_graph: None ) -> None:
   walk_route = ItineraryWalkRouteBuilder.build(
      _itinerary( SCHEDULED_LION ) )

   assert [ stop.item_key for stop in walk_route.stops ] == [
      ENTRANCE_ITEM_KEY,
      'African Lion||Africa Savanna||Outdoor',
      ENTRANCE_ITEM_KEY,
   ]
   assert len( walk_route.legs ) == 2
   assert walk_route.legs[ 0 ].from_item_key == ENTRANCE_ITEM_KEY
   assert walk_route.legs[ 0 ].to_item_key == 'African Lion||Africa Savanna||Outdoor'
   assert walk_route.legs[ 1 ].from_item_key == 'African Lion||Africa Savanna||Outdoor'
   assert walk_route.legs[ 1 ].to_item_key == ENTRANCE_ITEM_KEY
   assert len( walk_route.points ) == (
      len( walk_route.legs[ 0 ].node_ids )
      + len( walk_route.legs[ 1 ].node_ids )
      - 1
   )
   assert walk_route.points[ 0 ].node_id == walk_route.legs[ 0 ].node_ids[ 0 ]
   assert walk_route.points[ -1 ].node_id == walk_route.legs[ 1 ].node_ids[ -1 ]
   assert all(
      point.x_px >= 0 and point.y_px >= 0
      for point in walk_route.points )
