from __future__ import annotations

from .domain.loop_side_cluster_id import LoopSideClusterId
from .domain.master_route import MasterRoute


class MasterRouteLoopClusterIndexBuilder():
   @classmethod
   def side_cluster_id_by_loop_id(
         cls,
         master_route: MasterRoute ) -> dict[ str, LoopSideClusterId ]:
      indexes: dict[ str, LoopSideClusterId ] = {}

      for cluster in master_route.loop_side_clusters:
         for loop_id in cluster.loop_ids:
            indexes[ loop_id ] = cluster.cluster_id

      return indexes


   @classmethod
   def loop_index_in_side_cluster_by_loop_id(
         cls,
         master_route: MasterRoute ) -> dict[ str, int ]:
      indexes: dict[ str, int ] = {}

      for cluster in master_route.loop_side_clusters:
         for loop_index, loop_id in enumerate( cluster.loop_ids ):
            indexes[ loop_id ] = loop_index

      return indexes
