from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path

from .data_access.paths import Paths
from .domain.loop_side_cluster_id import LoopSideClusterId
from .domain.master_route import MasterRoute
from .domain.master_route_loop import MasterRouteLoop
from .domain.master_route_mapper import MasterRouteMapper
from .domain.master_route_stop_key import MasterRouteStopKey
from .master_route_loop_cluster_index_builder import MasterRouteLoopClusterIndexBuilder
from .master_route_stop_key_index_builder import MasterRouteStopKeyIndexBuilder


class MasterRouteProvider():
   @classmethod
   @lru_cache( maxsize=1 )
   def fetch_default( cls ) -> MasterRoute:
      return cls.fetch_from_file( Paths.DEFAULT_MASTER_ROUTE_PATH )


   @classmethod
   def fetch_from_file( cls, path: str ) -> MasterRoute:
      payload = json.loads( Path( path ).read_text( encoding='utf-8' ) )

      return MasterRouteMapper.map_record( payload )


   @classmethod
   @lru_cache( maxsize=1 )
   def loops_by_id( cls ) -> dict[ str, MasterRouteLoop ]:
      master_route = cls.fetch_default()

      return {
         loop.loop_id: loop
         for loop in master_route.loops
      }


   @classmethod
   @lru_cache( maxsize=1 )
   def route_index_by_stop_key( cls ) -> dict[ MasterRouteStopKey.Key, int ]:
      return MasterRouteStopKeyIndexBuilder.route_index( cls.fetch_default() )


   @classmethod
   @lru_cache( maxsize=1 )
   def loop_index_by_stop_key( cls ) -> dict[ MasterRouteStopKey.Key, int ]:
      return MasterRouteStopKeyIndexBuilder.loop_index( cls.fetch_default() )


   @classmethod
   @lru_cache( maxsize=1 )
   def loop_id_by_stop_key( cls ) -> dict[ MasterRouteStopKey.Key, str ]:
      return MasterRouteStopKeyIndexBuilder.loop_id( cls.fetch_default() )


   @classmethod
   @lru_cache( maxsize=1 )
   def loop_index_in_side_cluster_by_loop_id( cls ) -> dict[ str, int ]:
      return MasterRouteLoopClusterIndexBuilder.loop_index_in_side_cluster_by_loop_id(
         cls.fetch_default() )


   @classmethod
   @lru_cache( maxsize=1 )
   def loop_side_cluster_id_by_loop_id( cls ) -> dict[ str, LoopSideClusterId ]:
      return MasterRouteLoopClusterIndexBuilder.side_cluster_id_by_loop_id(
         cls.fetch_default() )
