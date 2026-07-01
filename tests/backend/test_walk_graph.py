from __future__ import annotations

from api.walk_graph.data_access.load_walk_graph import load_walk_graph


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


def test_walk_graph_entrance_is_the_parking_lot_spur_dead_end() -> None:
   graph = load_walk_graph()

   spur_nodes = [
      node
      for node in graph[ 'nodes' ]
      if node[ 'id' ] in { f'v-{ index:04d }' for index in range( 1, 8 ) }
   ]

   expected_entrance = max( spur_nodes, key=lambda node: node[ 'y_px' ] )

   assert graph[ 'entrance_node_id' ] == expected_entrance[ 'id' ]
   assert graph[ 'entrance_node_id' ] == 'v-0001'
