from __future__ import annotations

from api.walk_graph.loop_walk_endpoint_node_ids_resolver import LoopWalkEndpointNodeIdsResolver
from api.walk_graph.loop_walk_endpoint_node_ids_resolver import LoopWalkEndpointNodeIdsResolver
from api.walk_graph.master_route_provider import MasterRouteProvider


def test_loop_walk_endpoint_node_ids_use_first_and_last_master_route_spots() -> None:
   australasia_loop = MasterRouteProvider.loops_by_id()[ 'australasia' ]
   indo_malaya_loop = MasterRouteProvider.loops_by_id()[ 'indo_malaya' ]

   assert LoopWalkEndpointNodeIdsResolver.resolve( australasia_loop ) == ( 'v-1131', 'v-1061' )
   assert LoopWalkEndpointNodeIdsResolver.resolve( indo_malaya_loop ) == ( 'v-0226', 'v-0068' )


def test_loop_walk_endpoint_orientations_include_both_directions_for_two_way_loops() -> None:
   indo_malaya_loop = MasterRouteProvider.loops_by_id()[ 'indo_malaya' ]
   australasia_loop = MasterRouteProvider.loops_by_id()[ 'australasia' ]

   assert LoopWalkEndpointNodeIdsResolver.orientations( indo_malaya_loop ) == [
      ( 'v-0226', 'v-0068' ),
      ( 'v-0068', 'v-0226' ),
   ]
   assert LoopWalkEndpointNodeIdsResolver.orientations( australasia_loop ) == [
      ( 'v-1131', 'v-1061' ),
   ]
