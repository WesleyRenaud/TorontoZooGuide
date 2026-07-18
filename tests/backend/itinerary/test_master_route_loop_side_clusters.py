from __future__ import annotations

from api.walk_graph.master_route import default_loop_side_cluster_id_by_loop_id
from api.walk_graph.master_route import default_master_route


def test_default_master_route_loads_north_and_south_loop_side_clusters() -> None:
   master_route = default_master_route()

   assert len( master_route.loop_side_clusters ) == 2

   cluster_ids = {
      cluster.cluster_id
      for cluster in master_route.loop_side_clusters
   }
   assert cluster_ids == { 'north', 'south' }


def test_north_loop_side_cluster_contains_expected_loops() -> None:
   master_route = default_master_route()
   north_cluster = next(
      cluster
      for cluster in master_route.loop_side_clusters
      if cluster.cluster_id == 'north' )

   assert north_cluster.loop_ids == [
      'australasia',
      'discovery_zone',
      'eurasia',
      'tundra_trek_mayan_temple',
      'americas_pavilion',
   ]


def test_south_loop_side_cluster_contains_expected_loops() -> None:
   master_route = default_master_route()
   south_cluster = next(
      cluster
      for cluster in master_route.loop_side_clusters
      if cluster.cluster_id == 'south' )

   assert south_cluster.loop_ids == [
      'africa_savanna_canadian_domain',
      'african_rainforest_giraffe',
      'indo_malaya',
   ]


def test_default_loop_index_in_side_cluster_by_loop_id_maps_each_loop() -> None:
   from api.walk_graph.master_route import default_loop_index_in_side_cluster_by_loop_id

   loop_indexes = default_loop_index_in_side_cluster_by_loop_id()

   assert loop_indexes[ 'australasia' ] == 0
   assert loop_indexes[ 'eurasia' ] == 2
   assert loop_indexes[ 'tundra_trek_mayan_temple' ] == 3
   assert loop_indexes[ 'americas_pavilion' ] == 4
   assert loop_indexes[ 'indo_malaya' ] == 2


def test_default_loop_side_cluster_id_by_loop_id_maps_each_loop() -> None:
   loop_side_cluster_ids = default_loop_side_cluster_id_by_loop_id()

   assert loop_side_cluster_ids[ 'australasia' ] == 'north'
   assert loop_side_cluster_ids[ 'eurasia' ] == 'north'
   assert loop_side_cluster_ids[ 'discovery_zone' ] == 'north'
   assert loop_side_cluster_ids[ 'indo_malaya' ] == 'south'
   assert loop_side_cluster_ids[ 'africa_savanna_canadian_domain' ] == 'south'
   assert loop_side_cluster_ids[ 'african_rainforest_giraffe' ] == 'south'
