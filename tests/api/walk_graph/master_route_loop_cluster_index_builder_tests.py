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

   assert indexes[ LOOP_A ] == NORTH_CLUSTER.cluster_id
   assert indexes[ LOOP_B ] == NORTH_CLUSTER.cluster_id
   assert indexes[ LOOP_C ] == SOUTH_CLUSTER.cluster_id
   assert len( indexes ) == len( NORTH_CLUSTER.loop_ids ) + len( SOUTH_CLUSTER.loop_ids )


def Test_LoopIndexInSideClusterByLoopId_TestClusters_ExpectIndexes() -> None:
   indexes = MasterRouteLoopClusterIndexBuilder.loop_index_in_side_cluster_by_loop_id(
      MASTER_ROUTE )

   assert indexes[ LOOP_A ] == NORTH_CLUSTER.loop_ids.index( LOOP_A )
   assert indexes[ LOOP_B ] == NORTH_CLUSTER.loop_ids.index( LOOP_B )
   assert indexes[ LOOP_C ] == SOUTH_CLUSTER.loop_ids.index( LOOP_C )
   assert len( indexes ) == len( NORTH_CLUSTER.loop_ids ) + len( SOUTH_CLUSTER.loop_ids )
