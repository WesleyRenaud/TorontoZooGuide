from __future__ import annotations

from .master_route import MasterRoute
from .master_route_loop_mapper import MasterRouteLoopMapper
from .master_route_loop_side_cluster_mapper import MasterRouteLoopSideClusterMapper


class MasterRouteMapper():
   @classmethod
   def map_record( cls, payload: dict[ str, object ] ) -> MasterRoute:
      loop_side_clusters = [
         MasterRouteLoopSideClusterMapper.map_record( cluster )
         for cluster in payload.get( 'loop_side_clusters', [] )
      ]

      return MasterRoute(
         route_id=str( payload[ 'id' ] ),
         description=str( payload.get( 'description', '' ) ),
         loops=[
            MasterRouteLoopMapper.map_record( loop )
            for loop in payload[ 'loops' ]
         ],
         loop_side_clusters=loop_side_clusters )
