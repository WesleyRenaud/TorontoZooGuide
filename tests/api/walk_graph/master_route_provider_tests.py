from __future__ import annotations

import json
from pathlib import Path

import pytest

from api.walk_graph.domain.attraction_route_stop import AttractionRouteStop
from api.walk_graph.domain.loop_side_cluster_id import LoopSideClusterId
from api.walk_graph.domain.master_route import MasterRoute
from api.walk_graph.domain.master_route_loop import MasterRouteLoop, TWO_WAY_LOOP_TRAVERSAL
from api.walk_graph.domain.master_route_loop_side_cluster import MasterRouteLoopSideCluster
from api.walk_graph.domain.viewing_spot_reference import ViewingSpotReference
from api.walk_graph.master_route_provider import MasterRouteProvider

LION = ViewingSpotReference(
   species='African Lion',
   exhibit='Africa Savanna',
   name=None )
GIRAFFE = ViewingSpotReference(
   species='Masai Giraffe',
   exhibit='Africa Savanna',
   name=None )
CAROUSEL = AttractionRouteStop( name='Conservation Carousel' )

LOOP_AFRICA = MasterRouteLoop(
   loop_id='africa-loop',
   name='Africa',
   traversal=TWO_WAY_LOOP_TRAVERSAL,
   viewing_spots=[ LION, GIRAFFE ] )
LOOP_ATTRACTION = MasterRouteLoop(
   loop_id='carousel-loop',
   name='Carousel',
   traversal=TWO_WAY_LOOP_TRAVERSAL,
   viewing_spots=[ CAROUSEL ] )

MASTER_ROUTE = MasterRoute(
   route_id='main',
   description='Test route',
   loops=[ LOOP_AFRICA, LOOP_ATTRACTION ],
   loop_side_clusters=[
      MasterRouteLoopSideCluster(
         cluster_id=LoopSideClusterId.NORTH,
         loop_ids=[ 'africa-loop', 'carousel-loop' ] ),
   ] )

MASTER_ROUTE_PAYLOAD = {
   'id': 'main',
   'description': 'Test route',
   'loops': [
      {
         'id': 'africa-loop',
         'name': 'Africa',
         'traversal': 'two_way',
         'viewing_spots': [
            {
               'kind': 'animal',
               'key': [ 'African Lion', 'Africa Savanna', None ],
            },
            {
               'kind': 'animal',
               'key': [ 'Masai Giraffe', 'Africa Savanna', None ],
            },
         ],
      },
      {
         'id': 'carousel-loop',
         'name': 'Carousel',
         'traversal': 'two_way',
         'viewing_spots': [
            {
               'kind': 'attraction',
               'key': [ 'Conservation Carousel' ],
            },
         ],
      },
   ],
   'loop_side_clusters': [],
}

@pytest.fixture( autouse=True )
def clear_master_route_provider_cache() -> None:
   MasterRouteProvider.fetch_default.cache_clear()
   MasterRouteProvider.loops_by_id.cache_clear()
   MasterRouteProvider.route_index_by_stop_key.cache_clear()
   MasterRouteProvider.loop_index_by_stop_key.cache_clear()
   MasterRouteProvider.loop_id_by_stop_key.cache_clear()
   MasterRouteProvider.loop_index_in_side_cluster_by_loop_id.cache_clear()
   MasterRouteProvider.loop_side_cluster_id_by_loop_id.cache_clear()
   yield
   MasterRouteProvider.fetch_default.cache_clear()
   MasterRouteProvider.loops_by_id.cache_clear()
   MasterRouteProvider.route_index_by_stop_key.cache_clear()
   MasterRouteProvider.loop_index_by_stop_key.cache_clear()
   MasterRouteProvider.loop_id_by_stop_key.cache_clear()
   MasterRouteProvider.loop_index_in_side_cluster_by_loop_id.cache_clear()
   MasterRouteProvider.loop_side_cluster_id_by_loop_id.cache_clear()

def Test_FetchFromFile_TestJsonFile_ExpectMappedMasterRoute( tmp_path: Path ) -> None:
   route_path = tmp_path / 'master_route.json'
   route_path.write_text( json.dumps( MASTER_ROUTE_PAYLOAD ), encoding='utf-8' )

   route = MasterRouteProvider.fetch_from_file( str( route_path ) )

   assert route.route_id == 'main'
   assert [ loop.loop_id for loop in route.loops ] == [ 'africa-loop', 'carousel-loop' ]

def Test_LoopsById_TestDefaultRoute_ExpectLoopLookup(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( MasterRouteProvider, 'fetch_default', lambda: MASTER_ROUTE )

   loops_by_id = MasterRouteProvider.loops_by_id()

   assert set( loops_by_id ) == { 'africa-loop', 'carousel-loop' }
   assert loops_by_id[ 'africa-loop' ].name == 'Africa'

def Test_RouteIndexByStopKey_TestDefaultRoute_ExpectIndexes(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( MasterRouteProvider, 'fetch_default', lambda: MASTER_ROUTE )

   indexes = MasterRouteProvider.route_index_by_stop_key()

   assert indexes[ LION.master_route_key() ] == 0
   assert indexes[ CAROUSEL.master_route_key() ] == 2

def Test_LoopIndexByStopKey_TestDefaultRoute_ExpectLoopIndexes(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( MasterRouteProvider, 'fetch_default', lambda: MASTER_ROUTE )

   indexes = MasterRouteProvider.loop_index_by_stop_key()

   assert indexes[ LION.master_route_key() ] == 0
   assert indexes[ CAROUSEL.master_route_key() ] == 1

def Test_LoopIdByStopKey_TestDefaultRoute_ExpectLoopIds(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( MasterRouteProvider, 'fetch_default', lambda: MASTER_ROUTE )

   loop_ids = MasterRouteProvider.loop_id_by_stop_key()

   assert loop_ids[ LION.master_route_key() ] == 'africa-loop'
   assert loop_ids[ CAROUSEL.master_route_key() ] == 'carousel-loop'

def Test_LoopIndexInSideClusterByLoopId_TestDefaultRoute_ExpectIndexes(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( MasterRouteProvider, 'fetch_default', lambda: MASTER_ROUTE )

   indexes = MasterRouteProvider.loop_index_in_side_cluster_by_loop_id()

   assert indexes[ 'africa-loop' ] == 0
   assert indexes[ 'carousel-loop' ] == 1

def Test_LoopSideClusterIdByLoopId_TestDefaultRoute_ExpectClusterIds(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( MasterRouteProvider, 'fetch_default', lambda: MASTER_ROUTE )

   cluster_ids = MasterRouteProvider.loop_side_cluster_id_by_loop_id()

   assert cluster_ids[ 'africa-loop' ] == LoopSideClusterId.NORTH
   assert cluster_ids[ 'carousel-loop' ] == LoopSideClusterId.NORTH
