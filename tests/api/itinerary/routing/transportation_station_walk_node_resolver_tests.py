from __future__ import annotations

import pytest

from api.itinerary.routing.transportation_station_walk_node_resolver import TransportationStationWalkNodeResolver
from api.request_connection_provider import RequestConnectionProvider
from api.transportation.data_access.transportation_station_provider import TransportationStationProvider
from api.transportation.data_access.transportation_station_record import TransportationStationRecord
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode


ZOOMOBILE = 'Zoomobile'
MAIN_STATION = 'Main Zoomobile Station'
NEAR_NODE_ID = 'n-1'
FAR_NODE_ID = 'n-2'

STATION_RECORD = TransportationStationRecord(
   name=MAIN_STATION,
   description='Main boarding area',
   x_coord=90.0,
   y_coord=90.0 )


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
   'entrance_node_id': NEAR_NODE_ID,
   'nodes': [
      _node( NEAR_NODE_ID, 10.0, 10.0 ),
      _node( FAR_NODE_ID, 90.0, 90.0 ),
   ],
   'edges': [],
}


def _clear_walk_graph_provider_cache() -> None:
   WalkGraphProvider.fetch.cache_clear()


@pytest.fixture
def stub_transportation_station_walk_node_dependencies(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _clear_walk_graph_provider_cache()
   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: object() )
   monkeypatch.setattr(
      TransportationStationProvider,
      'fetch_transportation_station_record',
      lambda conn, transportation, station_name: (
         STATION_RECORD
         if transportation == ZOOMOBILE and station_name == MAIN_STATION
         else None ) )
   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: TEST_GRAPH )
   yield


def Test_Resolve_TestKnownStation_ExpectSnappedWalkNode(
      stub_transportation_station_walk_node_dependencies: None ) -> None:
   assert TransportationStationWalkNodeResolver.resolve(
      ZOOMOBILE,
      MAIN_STATION ) == FAR_NODE_ID


def Test_Resolve_TestMissingStationRecord_ExpectNone(
      stub_transportation_station_walk_node_dependencies: None ) -> None:
   assert TransportationStationWalkNodeResolver.resolve(
      ZOOMOBILE,
      'Unknown Station' ) is None
