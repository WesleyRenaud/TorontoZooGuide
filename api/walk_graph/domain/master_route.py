from __future__ import annotations

from dataclasses import dataclass, field

from .master_route_loop import master_route_loop_from_json
from .master_route_loop import MasterRouteLoop
from .master_route_loop_side_cluster import master_route_loop_side_cluster_from_json
from .master_route_loop_side_cluster import MasterRouteLoopSideCluster


@dataclass( frozen=True )
class MasterRoute:
   route_id: str
   description: str
   loops: list[ MasterRouteLoop ]
   loop_side_clusters: list[ MasterRouteLoopSideCluster ] = field( default_factory=list )


def master_route_from_json( payload: dict[ str, object ] ) -> MasterRoute:
   loop_side_clusters = [
      master_route_loop_side_cluster_from_json( cluster )
      for cluster in payload.get( 'loop_side_clusters', [] )
   ]

   return MasterRoute(
      route_id=str( payload[ 'id' ] ),
      description=str( payload.get( 'description', '' ) ),
      loops=[
         master_route_loop_from_json( loop )
         for loop in payload[ 'loops' ]
      ],
      loop_side_clusters=loop_side_clusters )
