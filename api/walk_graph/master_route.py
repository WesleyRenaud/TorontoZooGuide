from __future__ import annotations

from functools import lru_cache

from ..animals.search.animals_matching_query import viewing_spot_key_from_values
from .data_access.paths import DEFAULT_MASTER_ROUTE_PATH
from .domain.master_route import master_route_from_json
from .domain.master_route import MasterRoute
from .domain.master_route_loop import MasterRouteLoop
from .domain.viewing_spot_name_key import ViewingSpotNameKey
from .domain.viewing_spot_reference import ViewingSpotReference


def master_route_index_by_viewing_spot_key(
      master_route: MasterRoute ) -> dict[ ViewingSpotNameKey, int ]:
   indexes: dict[ ViewingSpotNameKey, int ] = {}
   route_index = 0

   for loop in master_route.loops:
      for viewing_spot in loop.viewing_spots:
         viewing_spot_key = viewing_spot_key_from_reference( viewing_spot )

         if viewing_spot_key in indexes:
            continue

         indexes[ viewing_spot_key ] = route_index
         route_index += 1

   return indexes


def loop_index_by_viewing_spot_key(
      master_route: MasterRoute ) -> dict[ ViewingSpotNameKey, int ]:
   indexes: dict[ ViewingSpotNameKey, int ] = {}

   for loop_index, loop in enumerate( master_route.loops ):
      for viewing_spot in loop.viewing_spots:
         viewing_spot_key = viewing_spot_key_from_reference( viewing_spot )
         indexes.setdefault( viewing_spot_key, loop_index )

   return indexes


def viewing_spot_key_from_reference(
      viewing_spot: ViewingSpotReference ) -> ViewingSpotNameKey:
   return viewing_spot_key_from_values(
      viewing_spot.species,
      viewing_spot.exhibit,
      viewing_spot.name )


@lru_cache( maxsize=1 )
def default_master_route() -> MasterRoute:
   return master_route_from_json_file( DEFAULT_MASTER_ROUTE_PATH )


@lru_cache( maxsize=1 )
def default_master_route_index_by_viewing_spot_key() -> dict[
      ViewingSpotNameKey,
      int,
   ]:
   return master_route_index_by_viewing_spot_key( default_master_route() )


def loop_id_by_viewing_spot_key(
      master_route: MasterRoute ) -> dict[ ViewingSpotNameKey, str ]:
   indexes: dict[ ViewingSpotNameKey, str ] = {}

   for loop in master_route.loops:
      for viewing_spot in loop.viewing_spots:
         viewing_spot_key = viewing_spot_key_from_reference( viewing_spot )
         indexes.setdefault( viewing_spot_key, loop.loop_id )

   return indexes


@lru_cache( maxsize=1 )
def default_loop_id_by_viewing_spot_key() -> dict[ ViewingSpotNameKey, str ]:
   return loop_id_by_viewing_spot_key( default_master_route() )


@lru_cache( maxsize=1 )
def default_loop_index_by_viewing_spot_key() -> dict[ ViewingSpotNameKey, int ]:
   return loop_index_by_viewing_spot_key( default_master_route() )


def loop_side_cluster_id_by_loop_id(
      master_route: MasterRoute ) -> dict[ str, str ]:
   indexes: dict[ str, str ] = {}

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
def default_loop_side_cluster_id_by_loop_id() -> dict[ str, str ]:
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
