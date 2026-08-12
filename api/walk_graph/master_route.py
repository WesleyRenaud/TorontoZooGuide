from __future__ import annotations

from functools import lru_cache

from .data_access.paths import DEFAULT_MASTER_ROUTE_PATH
from .domain.loop_side_cluster_id import LoopSideClusterId
from .domain.master_route import master_route_from_json
from .domain.master_route import MasterRoute
from .domain.master_route_loop import MasterRouteLoop
from .domain.master_route_stop import master_route_stop_key
from .domain.master_route_stop_key import MasterRouteStopKey


def master_route_index_by_stop_key(
      master_route: MasterRoute ) -> dict[ MasterRouteStopKey, int ]:
   indexes: dict[ MasterRouteStopKey, int ] = {}
   route_index = 0

   for loop in master_route.loops:
      for stop in loop.viewing_spots:
         stop_key = master_route_stop_key( stop )

         if stop_key in indexes:
            continue

         indexes[ stop_key ] = route_index
         route_index += 1

   return indexes


def loop_index_by_stop_key(
      master_route: MasterRoute ) -> dict[ MasterRouteStopKey, int ]:
   indexes: dict[ MasterRouteStopKey, int ] = {}

   for loop_index, loop in enumerate( master_route.loops ):
      for stop in loop.viewing_spots:
         indexes.setdefault( master_route_stop_key( stop ), loop_index )

   return indexes


def loop_id_by_stop_key(
      master_route: MasterRoute ) -> dict[ MasterRouteStopKey, str ]:
   indexes: dict[ MasterRouteStopKey, str ] = {}

   for loop in master_route.loops:
      for stop in loop.viewing_spots:
         indexes.setdefault( master_route_stop_key( stop ), loop.loop_id )

   return indexes


@lru_cache( maxsize=1 )
def default_master_route() -> MasterRoute:
   return master_route_from_json_file( DEFAULT_MASTER_ROUTE_PATH )


@lru_cache( maxsize=1 )
def default_master_route_index_by_stop_key() -> dict[ MasterRouteStopKey, int ]:
   return master_route_index_by_stop_key( default_master_route() )


@lru_cache( maxsize=1 )
def default_loop_index_by_stop_key() -> dict[ MasterRouteStopKey, int ]:
   return loop_index_by_stop_key( default_master_route() )


@lru_cache( maxsize=1 )
def default_loop_id_by_stop_key() -> dict[ MasterRouteStopKey, str ]:
   return loop_id_by_stop_key( default_master_route() )


def loop_side_cluster_id_by_loop_id(
      master_route: MasterRoute ) -> dict[ str, LoopSideClusterId ]:
   indexes: dict[ str, LoopSideClusterId ] = {}

   for cluster in master_route.loop_side_clusters:
      for loop_id in cluster.loop_ids:
         indexes[ loop_id ] = cluster.cluster_id

   return indexes


def loop_index_in_side_cluster_by_loop_id(
      master_route: MasterRoute ) -> dict[ str, int ]:
   indexes: dict[ str, int ] = {}

   for cluster in master_route.loop_side_clusters:
      for loop_index, loop_id in enumerate( cluster.loop_ids ):
         indexes[ loop_id ] = loop_index

   return indexes


@lru_cache( maxsize=1 )
def default_loop_index_in_side_cluster_by_loop_id() -> dict[ str, int ]:
   return loop_index_in_side_cluster_by_loop_id( default_master_route() )


@lru_cache( maxsize=1 )
def default_loop_side_cluster_id_by_loop_id() -> dict[ str, LoopSideClusterId ]:
   return loop_side_cluster_id_by_loop_id( default_master_route() )


@lru_cache( maxsize=1 )
def default_master_route_loop_by_id() -> dict[ str, MasterRouteLoop ]:
   master_route = default_master_route()

   return {
      loop.loop_id: loop
      for loop in master_route.loops
   }


def master_route_from_json_file( path: str ) -> MasterRoute:
   import json
   from pathlib import Path

   payload = json.loads( Path( path ).read_text( encoding='utf-8' ) )

   return master_route_from_json( payload )
