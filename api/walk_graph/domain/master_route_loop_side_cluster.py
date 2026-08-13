from __future__ import annotations

from dataclasses import dataclass

from .loop_side_cluster_id import LoopSideClusterId


@dataclass( frozen=True )
class MasterRouteLoopSideCluster:
   cluster_id: LoopSideClusterId
   loop_ids: list[ str ]


def master_route_loop_side_cluster_from_json(
      payload: dict[ str, object ] ) -> MasterRouteLoopSideCluster:
   return MasterRouteLoopSideCluster(
      cluster_id=LoopSideClusterId( str( payload[ 'id' ] ) ),
      loop_ids=[
         str( loop_id )
         for loop_id in payload[ 'loop_ids' ]
      ] )
