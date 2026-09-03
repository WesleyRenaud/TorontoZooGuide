from __future__ import annotations

from api.walk_graph.domain.attraction_route_stop import AttractionRouteStop
from api.walk_graph.domain.master_route import MasterRoute
from api.walk_graph.domain.master_route_loop import MasterRouteLoop, TWO_WAY_LOOP_TRAVERSAL
from api.walk_graph.domain.viewing_spot_reference import ViewingSpotReference
from api.walk_graph.master_route_stop_key_index_builder import MasterRouteStopKeyIndexBuilder

LION = ViewingSpotReference(
   species='African Lion',
   exhibit='Africa Savanna',
   name=None )
GIRAFFE = ViewingSpotReference(
   species='Masai Giraffe',
   exhibit='Africa Savanna',
   name=None )
CAROUSEL = AttractionRouteStop( name='Conservation Carousel' )
LION_DUPLICATE = ViewingSpotReference(
   species='African Lion',
   exhibit='Africa Savanna',
   name=None )

LOOP_AFRICA = MasterRouteLoop(
   loop_id='africa-loop',
   name='Africa',
   traversal=TWO_WAY_LOOP_TRAVERSAL,
   viewing_spots=[ LION, GIRAFFE, LION_DUPLICATE ] )
LOOP_ATTRACTION = MasterRouteLoop(
   loop_id='carousel-loop',
   name='Carousel',
   traversal=TWO_WAY_LOOP_TRAVERSAL,
   viewing_spots=[ CAROUSEL, LION ] )

MASTER_ROUTE = MasterRoute(
   route_id='main',
   description='Test route',
   loops=[ LOOP_AFRICA, LOOP_ATTRACTION ] )

def Test_RouteIndex_TestDuplicateStopKeys_ExpectFirstOccurrenceIndexes() -> None:
   indexes = MasterRouteStopKeyIndexBuilder.route_index( MASTER_ROUTE )

   assert indexes[ LION.master_route_key() ] == 0
   assert indexes[ GIRAFFE.master_route_key() ] == 1
   assert indexes[ CAROUSEL.master_route_key() ] == 2
   assert len( indexes ) == 3

def Test_LoopIndex_TestDuplicateAcrossLoops_ExpectFirstLoopIndex() -> None:
   indexes = MasterRouteStopKeyIndexBuilder.loop_index( MASTER_ROUTE )

   assert indexes[ LION.master_route_key() ] == 0
   assert indexes[ GIRAFFE.master_route_key() ] == 0
   assert indexes[ CAROUSEL.master_route_key() ] == 1

def Test_LoopId_TestDuplicateAcrossLoops_ExpectFirstLoopId() -> None:
   indexes = MasterRouteStopKeyIndexBuilder.loop_id( MASTER_ROUTE )

   assert indexes[ LION.master_route_key() ] == 'africa-loop'
   assert indexes[ GIRAFFE.master_route_key() ] == 'africa-loop'
   assert indexes[ CAROUSEL.master_route_key() ] == 'carousel-loop'
