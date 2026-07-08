from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class MasterRouteLoopSideCluster:
   cluster_id: str
   loop_ids: tuple[ str, ... ]


def master_route_loop_side_cluster_from_json(
      payload: dict[ str, object ] ) -> MasterRouteLoopSideCluster:
   return MasterRouteLoopSideCluster(
      cluster_id=str( payload[ 'id' ] ),
      loop_ids=tuple(
         str( loop_id )
         for loop_id in payload[ 'loop_ids' ] ) )
