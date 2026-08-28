from __future__ import annotations

from .loop_side_cluster_id import LoopSideClusterId
from .master_route_loop_side_cluster import MasterRouteLoopSideCluster


class MasterRouteLoopSideClusterMapper():
   @classmethod
   def map_record(
         cls,
         payload: dict[ str, object ] ) -> MasterRouteLoopSideCluster:
      return MasterRouteLoopSideCluster(
         cluster_id=LoopSideClusterId( str( payload[ 'id' ] ) ),
         loop_ids=[
            str( loop_id )
            for loop_id in payload[ 'loop_ids' ]
         ] )
