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
      'splash_island',
      'eurasia',
      'eurasia_attractions',
      'tundra_trek_mayan_temple',
      'tundra_attractions',
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
      'gorilla_climb',
      'indo_malaya',
      'conservation_carousel',
      'zoomobile',
   ]


def test_default_loop_index_in_side_cluster_by_loop_id_maps_each_loop() -> None:
   from api.walk_graph.master_route import default_loop_index_in_side_cluster_by_loop_id

   loop_indexes = default_loop_index_in_side_cluster_by_loop_id()

   assert loop_indexes[ 'australasia' ] == 0
   assert loop_indexes[ 'splash_island' ] == 2
   assert loop_indexes[ 'eurasia' ] == 3
   assert loop_indexes[ 'eurasia_attractions' ] == 4
   assert loop_indexes[ 'tundra_trek_mayan_temple' ] == 5
   assert loop_indexes[ 'tundra_attractions' ] == 6
   assert loop_indexes[ 'americas_pavilion' ] == 7
   assert loop_indexes[ 'gorilla_climb' ] == 2
   assert loop_indexes[ 'indo_malaya' ] == 3
   assert loop_indexes[ 'conservation_carousel' ] == 4
   assert loop_indexes[ 'zoomobile' ] == 5


def test_default_loop_side_cluster_id_by_loop_id_maps_each_loop() -> None:
   loop_side_cluster_ids = default_loop_side_cluster_id_by_loop_id()

   assert loop_side_cluster_ids[ 'australasia' ] == 'north'
   assert loop_side_cluster_ids[ 'eurasia' ] == 'north'
   assert loop_side_cluster_ids[ 'discovery_zone' ] == 'north'
   assert loop_side_cluster_ids[ 'splash_island' ] == 'north'
   assert loop_side_cluster_ids[ 'eurasia_attractions' ] == 'north'
   assert loop_side_cluster_ids[ 'tundra_attractions' ] == 'north'
   assert loop_side_cluster_ids[ 'indo_malaya' ] == 'south'
   assert loop_side_cluster_ids[ 'africa_savanna_canadian_domain' ] == 'south'
   assert loop_side_cluster_ids[ 'african_rainforest_giraffe' ] == 'south'
   assert loop_side_cluster_ids[ 'gorilla_climb' ] == 'south'
   assert loop_side_cluster_ids[ 'conservation_carousel' ] == 'south'
   assert loop_side_cluster_ids[ 'zoomobile' ] == 'south'
