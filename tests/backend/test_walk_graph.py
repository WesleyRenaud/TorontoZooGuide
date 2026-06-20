from __future__ import annotations

from collections import defaultdict
import json
import math
from pathlib import Path


ROOT = Path( __file__ ).resolve().parents[ 2 ]
WALK_GRAPH_PATH = ROOT / 'api' / 'seed' / 'data' / 'walk_graph.json'


def load_walk_graph() -> dict[ str, object ]:
   return json.loads( WALK_GRAPH_PATH.read_text( encoding='utf-8' ) )


def test_walk_graph_has_nodes_edges_and_entrance() -> None:
   graph = load_walk_graph()

   assert graph[ 'map_width_px' ] == 4096
   assert graph[ 'map_height_px' ] == 2665
   assert isinstance( graph[ 'nodes' ], list )
   assert isinstance( graph[ 'edges' ], list )
   assert graph[ 'nodes' ]
   assert graph[ 'edges' ]
   assert graph[ 'entrance_node_id' ]


def test_walk_graph_node_and_edge_references_are_valid() -> None:
   graph = load_walk_graph()
   node_ids = { node[ 'id' ] for node in graph[ 'nodes' ] }

   assert graph[ 'entrance_node_id' ] in node_ids

   for edge in graph[ 'edges' ]:
      assert edge[ 'from' ] in node_ids
      assert edge[ 'to' ] in node_ids
      assert edge[ 'length_px' ] > 0


def test_walk_graph_entrance_is_a_dead_end_near_the_entrance_landmark() -> None:
   graph = load_walk_graph()
   degrees: dict[ str, int ] = defaultdict( int )

   for edge in graph[ 'edges' ]:
      degrees[ edge[ 'from' ] ] += 1
      degrees[ edge[ 'to' ] ] += 1

   entrance_id = graph[ 'entrance_node_id' ]
   assert degrees[ entrance_id ] == 1

   landmark = graph[ 'entrance_landmark' ]
   landmark_x_px = landmark[ 'x' ] / 100 * graph[ 'map_width_px' ]
   landmark_y_px = landmark[ 'y' ] / 100 * graph[ 'map_height_px' ]

   dead_ends = [
      node
      for node in graph[ 'nodes' ]
      if degrees[ node[ 'id' ] ] == 1
   ]

   expected_entrance = min(
      dead_ends,
      key=lambda node: (
         math.hypot(
            node[ 'x_px' ] - landmark_x_px,
            node[ 'y_px' ] - landmark_y_px ),
         -node[ 'y' ],
      ) )

   assert entrance_id == expected_entrance[ 'id' ]
