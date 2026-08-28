from __future__ import annotations

from dataclasses import dataclass

from .loop_side_cluster_id import LoopSideClusterId


@dataclass( frozen=True )
class MasterRouteLoopSideCluster:
   cluster_id: LoopSideClusterId
   loop_ids: list[ str ]
