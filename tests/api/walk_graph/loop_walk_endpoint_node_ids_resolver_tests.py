from __future__ import annotations

import pytest

from api.shared.enums import ScheduleItemKind
from api.walk_graph.domain.attraction_route_stop import AttractionRouteStop
from api.walk_graph.domain.map_location_kind import MapLocationKind
from api.walk_graph.domain.map_location_walk_node import MapLocationWalkNode
from api.walk_graph.domain.master_route_loop import MasterRouteLoop
from api.walk_graph.domain.master_route_loop import ONE_WAY_LOOP_TRAVERSAL
from api.walk_graph.domain.master_route_loop import TWO_WAY_LOOP_TRAVERSAL
from api.walk_graph.domain.viewing_spot_reference import ViewingSpotReference
from api.walk_graph.loop_walk_endpoint_node_ids_resolver import LoopWalkEndpointNodeIdsResolver
from api.walk_graph.map_location_walk_node_lookup import MapLocationWalkNodeLookup
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver


AUSTRALASIA_FIRST_NODE_ID = 'n-aus-first'
AUSTRALASIA_LAST_NODE_ID = 'n-aus-last'
INDO_FIRST_NODE_ID = 'n-indo-first'
INDO_LAST_NODE_ID = 'n-indo-last'
CAROUSEL_NODE_ID = 'n-carousel'

AUSTRALASIA_LOOP = MasterRouteLoop(
   loop_id='australasia',
   name='Australasia',
   traversal=ONE_WAY_LOOP_TRAVERSAL,
   viewing_spots=[
      ViewingSpotReference(
         species='Kookaburra',
         exhibit='Australasia Pavilion',
         name='Indoor' ),
      ViewingSpotReference(
         species='Amur Tiger',
         exhibit='Eurasia Wilds',
         name=None ),
   ] )

INDO_MALAYA_LOOP = MasterRouteLoop(
   loop_id='indo_malaya',
   name='Indo-Malaya',
   traversal=TWO_WAY_LOOP_TRAVERSAL,
   viewing_spots=[
      ViewingSpotReference(
         species='Cheetah',
         exhibit='Indo-Malaya Outdoor',
         name=None ),
      ViewingSpotReference(
         species='Orangutan',
         exhibit='Indo-Malaya Pavilion',
         name='Indoor' ),
   ] )

EMPTY_LOOP = MasterRouteLoop(
   loop_id='empty',
   name='Empty',
   traversal=ONE_WAY_LOOP_TRAVERSAL,
   viewing_spots=[] )

ATTRACTION_LOOP = MasterRouteLoop(
   loop_id='attractions',
   name='Attractions',
   traversal=ONE_WAY_LOOP_TRAVERSAL,
   viewing_spots=[
      AttractionRouteStop( name='Conservation Carousel' ),
      AttractionRouteStop( name='Splash Island' ),
   ] )

WALK_NODE_IDS = {
   ( 'Kookaburra', 'Australasia Pavilion', 'Indoor' ): AUSTRALASIA_FIRST_NODE_ID,
   ( 'Amur Tiger', 'Eurasia Wilds', None ): AUSTRALASIA_LAST_NODE_ID,
   ( 'Cheetah', 'Indo-Malaya Outdoor', None ): INDO_FIRST_NODE_ID,
   ( 'Orangutan', 'Indo-Malaya Pavilion', 'Indoor' ): INDO_LAST_NODE_ID,
}

CAROUSEL_WALK_NODE = MapLocationWalkNode(
   kind=MapLocationKind.ATTRACTION,
   name='Conservation Carousel',
   location='',
   x=1.0,
   y=2.0,
   walk_node_id=CAROUSEL_NODE_ID,
   snap_distance_px=5.0 )


@pytest.fixture
def stub_viewing_spot_walk_nodes( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ViewingSpotWalkNodeIdResolver,
      'resolve',
      lambda species, exhibit, enclosure_name=None: WALK_NODE_IDS.get(
         ( species, exhibit, enclosure_name ) ) )


def Test_Resolve_TestMasterRouteLoops_ExpectFirstAndLastWalkNodes(
      stub_viewing_spot_walk_nodes: None ) -> None:
   assert LoopWalkEndpointNodeIdsResolver.resolve( AUSTRALASIA_LOOP ) == (
      AUSTRALASIA_FIRST_NODE_ID,
      AUSTRALASIA_LAST_NODE_ID )
   assert LoopWalkEndpointNodeIdsResolver.resolve( INDO_MALAYA_LOOP ) == (
      INDO_FIRST_NODE_ID,
      INDO_LAST_NODE_ID )


def Test_Orientations_TestTraversalKinds_ExpectForwardAndReversePairs(
      stub_viewing_spot_walk_nodes: None ) -> None:
   assert LoopWalkEndpointNodeIdsResolver.orientations( INDO_MALAYA_LOOP ) == [
      ( INDO_FIRST_NODE_ID, INDO_LAST_NODE_ID ),
      ( INDO_LAST_NODE_ID, INDO_FIRST_NODE_ID ),
   ]
   assert LoopWalkEndpointNodeIdsResolver.orientations( AUSTRALASIA_LOOP ) == [
      ( AUSTRALASIA_FIRST_NODE_ID, AUSTRALASIA_LAST_NODE_ID ),
   ]


def Test_Resolve_TestEmptyViewingSpots_ExpectNonePair() -> None:
   assert LoopWalkEndpointNodeIdsResolver.resolve( EMPTY_LOOP ) == ( None, None )


def Test_Resolve_TestAttractionStops_ExpectWalkNodeIds(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   def for_map_location(
         kind: MapLocationKind,
         name: str,
         *,
         location: str = '' ) -> MapLocationWalkNode | None:
      if kind == MapLocationKind.ATTRACTION and name == 'Conservation Carousel':
         return CAROUSEL_WALK_NODE

      return None

   monkeypatch.setattr(
      MapLocationWalkNodeLookup,
      'for_map_location',
      for_map_location )

   assert LoopWalkEndpointNodeIdsResolver.resolve( ATTRACTION_LOOP ) == (
      CAROUSEL_NODE_ID,
      None )


def Test_WalkNodeIdForRouteStop_TestUnknownKind_ExpectNone() -> None:
   class _UnknownStop:
      kind = ScheduleItemKind.ENTRANCE

   assert LoopWalkEndpointNodeIdsResolver._walk_node_id_for_route_stop(
      _UnknownStop() ) is None
