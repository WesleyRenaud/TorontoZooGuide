from __future__ import annotations

from dataclasses import dataclass, field

from .master_route_loop import MasterRouteLoop
from .master_route_loop_side_cluster import MasterRouteLoopSideCluster


@dataclass( frozen=True )
class MasterRoute:
   route_id: str
   description: str
   loops: list[ MasterRouteLoop ]
   loop_side_clusters: list[ MasterRouteLoopSideCluster ] = field( default_factory=list )
