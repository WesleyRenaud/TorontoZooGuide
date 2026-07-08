from __future__ import annotations

from api.walk_graph.loop_walk_endpoint_node_ids import loop_walk_endpoint_node_ids
from api.walk_graph.master_route import default_master_route_loop_by_id


def test_loop_walk_endpoint_node_ids_use_first_and_last_master_route_spots() -> None:
   australasia_loop = default_master_route_loop_by_id()[ 'australasia' ]
   indo_malaya_loop = default_master_route_loop_by_id()[ 'indo_malaya' ]

   assert loop_walk_endpoint_node_ids( australasia_loop ) == ( 'v-1131', 'v-1061' )
   assert loop_walk_endpoint_node_ids( indo_malaya_loop ) == ( 'v-0226', 'v-0068' )
