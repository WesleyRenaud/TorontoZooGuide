from __future__ import annotations

import json
from pathlib import Path

import pytest

from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode


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
   'entrance_node_id': 'n-1',
   'nodes': [
      _node( 'n-1', 0.0, 0.0 ),
      _node( 'n-2', 10.0, 0.0 ),
      _node( 'n-3', 20.0, 0.0 ),
   ],
   'edges': [
      { 'from': 'n-1', 'to': 'n-2', 'length_px': 10.0 },
      { 'from': 'n-2', 'to': 'n-3', 'length_px': 20.0 },
   ],
}


@pytest.fixture( autouse=True )
def clear_walk_graph_provider_cache() -> None:
   WalkGraphProvider.fetch.cache_clear()
   yield
   WalkGraphProvider.fetch.cache_clear()


def Test_Fetch_TestJsonFile_ExpectParsedWalkGraph( tmp_path: Path ) -> None:
   graph_path = tmp_path / 'walk_graph.json'
   graph_path.write_text( json.dumps( TEST_GRAPH ), encoding='utf-8' )

   assert WalkGraphProvider.fetch( path=graph_path ) == TEST_GRAPH


def Test_Fetch_TestJsonFile_ExpectValidNodeAndEdgeReferences( tmp_path: Path ) -> None:
   graph_path = tmp_path / 'walk_graph.json'
   graph_path.write_text( json.dumps( TEST_GRAPH ), encoding='utf-8' )
   graph = WalkGraphProvider.fetch( path=graph_path )
   node_ids = { node[ 'id' ] for node in graph[ 'nodes' ] }

   assert graph[ 'entrance_node_id' ] in node_ids

   for edge in graph[ 'edges' ]:
      assert edge[ 'from' ] in node_ids
      assert edge[ 'to' ] in node_ids
      assert edge[ 'length_px' ] > 0
