from __future__ import annotations

from api.walk_graph.domain.loop_side_cluster_id import LoopSideClusterId
from api.walk_graph.domain.master_route import MasterRoute
from api.walk_graph.domain.master_route_loop_side_cluster import MasterRouteLoopSideCluster
from api.walk_graph.master_route_loop_cluster_index_builder import MasterRouteLoopClusterIndexBuilder

LOOP_A = 'africa-savanna'
LOOP_B = 'africa-rainforest'
LOOP_C = 'canadian-domain'

NORTH_CLUSTER = MasterRouteLoopSideCluster(
   cluster_id=LoopSideClusterId.NORTH,
   loop_ids=[ LOOP_A, LOOP_B ] )
SOUTH_CLUSTER = MasterRouteLoopSideCluster(
   cluster_id=LoopSideClusterId.SOUTH,
   loop_ids=[ LOOP_C ] )

MASTER_ROUTE = MasterRoute(
   route_id='main',
   description='Test route',
   loops=[],
   loop_side_clusters=[ NORTH_CLUSTER, SOUTH_CLUSTER ] )

def Test_SideClusterIdByLoopId_TestClusters_ExpectMapped() -> None:
   indexes = MasterRouteLoopClusterIndexBuilder.side_cluster_id_by_loop_id( MASTER_ROUTE )

   assert indexes[ LOOP_A ] == LoopSideClusterId.NORTH
   assert indexes[ LOOP_B ] == LoopSideClusterId.NORTH
   assert indexes[ LOOP_C ] == LoopSideClusterId.SOUTH
   assert len( indexes ) == 3

def Test_LoopIndexInSideClusterByLoopId_TestClusters_ExpectIndexes() -> None:
   indexes = MasterRouteLoopClusterIndexBuilder.loop_index_in_side_cluster_by_loop_id( MASTER_ROUTE )

   assert indexes[ LOOP_A ] == 0
   assert indexes[ LOOP_B ] == 1
   assert indexes[ LOOP_C ] == 0
   assert len( indexes ) == 3
