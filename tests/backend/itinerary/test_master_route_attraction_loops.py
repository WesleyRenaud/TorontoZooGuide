from __future__ import annotations

from api.walk_graph.domain.attraction_route_stop import AttractionRouteStop
from api.walk_graph.domain.master_route_stop_checker import MasterRouteStopChecker
from api.walk_graph.loop_walk_endpoint_node_ids_resolver import LoopWalkEndpointNodeIdsResolver
from api.walk_graph.master_route_provider import MasterRouteProvider


def test_default_master_route_loops_fit_attractions_in_route_order() -> None:
   master_route = MasterRouteProvider.fetch_default()
   loop_ids = [ loop.loop_id for loop in master_route.loops ]

   assert loop_ids == [
      'australasia',
      'eurasia',
      'eurasia_attractions',
      'tundra_trek_mayan_temple',
      'tundra_attractions',
      'americas_pavilion',
      'africa_savanna_canadian_domain',
      'african_rainforest_giraffe',
      'gorilla_climb',
      'indo_malaya',
      'conservation_carousel',
      'face_painting_front_gates',
      'discovery_zone',
      'splash_island',
      'zoomobile',
   ]
   assert loop_ids[ -1 ] == 'zoomobile'
   assert loop_ids.index( 'tundra_attractions' ) == (
      loop_ids.index( 'tundra_trek_mayan_temple' ) + 1 )


def test_default_master_route_includes_attraction_loops() -> None:
   loops_by_id = MasterRouteProvider.loops_by_id()

   assert [
      stop.name
      for stop in loops_by_id[ 'eurasia_attractions' ].viewing_spots
      if MasterRouteStopChecker.is_attraction( stop )
   ] == [
      'Greenhouse',
      'Wildlife Health & Science Centre',
   ]
   assert [
      stop.name
      for stop in loops_by_id[ 'tundra_attractions' ].viewing_spots
      if MasterRouteStopChecker.is_attraction( stop )
   ] == [
      'TundraAir Ride',
      'Face Painting, Caricatures and Henna! - Tundra Trek',
      'Virtual Reality (VR) Theatre!',
   ]
   assert isinstance(
      loops_by_id[ 'splash_island' ].viewing_spots[ 0 ],
      AttractionRouteStop )
   assert loops_by_id[ 'splash_island' ].viewing_spots[ 0 ].name == 'Splash Island'
   assert loops_by_id[ 'gorilla_climb' ].viewing_spots[ 0 ].name == (
      'Gorilla Climb Ropes Course' )
   assert loops_by_id[ 'conservation_carousel' ].viewing_spots[ 0 ].name == (
      'Conservation Carousel' )
   assert loops_by_id[ 'face_painting_front_gates' ].viewing_spots[ 0 ].name == (
      'Face Painting, Caricatures and Henna! - Front Gates' )
   assert loops_by_id[ 'zoomobile' ].viewing_spots[ 0 ].name == 'Zoomobile'


def test_kangaroo_walk_thru_is_woven_into_australasia_loop() -> None:
   australasia = MasterRouteProvider.loops_by_id()[ 'australasia' ]
   stops = australasia.viewing_spots

   kangaroo_index = next(
      index
      for index, stop in enumerate( stops )
      if (
         not MasterRouteStopChecker.is_attraction( stop )
         and stop.species == 'Western Grey Kangaroo' ) )
   walk_thru = stops[ kangaroo_index + 1 ]
   tiger = stops[ kangaroo_index + 2 ]

   assert isinstance( walk_thru, AttractionRouteStop )
   assert walk_thru.name == 'Kangaroo Walk-Thru'
   assert not MasterRouteStopChecker.is_attraction( tiger )
   assert tiger.species == 'Amur Tiger'


def test_attraction_loop_walk_endpoints_use_attraction_walk_nodes() -> None:
   eurasia_attractions = MasterRouteProvider.loops_by_id()[ 'eurasia_attractions' ]

   assert LoopWalkEndpointNodeIdsResolver.resolve( eurasia_attractions ) == (
      'v-0889',
      'v-0894',
   )
