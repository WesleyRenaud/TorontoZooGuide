from __future__ import annotations

import pytest

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.routing.itinerary_stop import ENTRANCE_ITEM_KEY
from api.itinerary.routing.itinerary_walk_route_builder import ItineraryWalkRouteBuilder
from api.itinerary.routing.transit_ride_endpoint import TransitRideEndpoint
from api.itinerary.routing.walk_route_anchor import WalkRouteAnchor
from api.itinerary.routing.walk_route_anchor_builder import WalkRouteAnchorBuilder
from api.models import Animal
from api.models import Itinerary
from api.shared.enums import ScheduleItemKind
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode
from api.walk_graph.representative_walk_node_resolver import RepresentativeWalkNodeResolver
from api.walk_graph.shortest_path_calculator import ShortestPathCalculator
from api.walk_graph.viewing_walk_node_id_resolver import ViewingWalkNodeIdResolver


VISIT_DATE = '2026-06-20'
ARRIVAL_TIME = '9:30 AM'
DEPARTURE_TIME = '5:00 PM'

ENTRANCE_NODE_ID = 'n-1'
LION_WALK_NODE_ID = 'n-2'


def _node( node_id: str, x_px: float, y_px: float ) -> WalkGraphNode:
   return {
      'id': node_id,
      'x': x_px / 100.0,
      'y': y_px / 100.0,
      'x_px': x_px,
      'y_px': y_px,
   }


TEST_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': ENTRANCE_NODE_ID,
   'nodes': [
      _node( ENTRANCE_NODE_ID, 0.0, 0.0 ),
      _node( LION_WALK_NODE_ID, 10.0, 0.0 ),
   ],
   'edges': [
      { 'from': ENTRANCE_NODE_ID, 'to': LION_WALK_NODE_ID, 'length_px': 10.0 },
      { 'from': LION_WALK_NODE_ID, 'to': ENTRANCE_NODE_ID, 'length_px': 10.0 },
   ],
}

UNSCHEDULED_LION = Animal(
   species='African Lion',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
   enclosure_type='Outdoor',
   x_coord=10.0,
   y_coord=0.0,
)

SCHEDULED_LION = Animal(
   species='African Lion',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
   enclosure_type='Outdoor',
   x_coord=10.0,
   y_coord=0.0,
   start_time='10:00 AM',
   end_time='10:30 AM',
)


def _clear_walk_graph_provider_cache() -> None:
   WalkGraphProvider.fetch.cache_clear()


@pytest.fixture
def stub_walk_graph( monkeypatch: pytest.MonkeyPatch ) -> None:
   _clear_walk_graph_provider_cache()
   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: TEST_GRAPH )
   monkeypatch.setattr(
      ViewingWalkNodeIdResolver,
      'resolve',
      lambda *args, **kwargs: LION_WALK_NODE_ID )
   yield


def _itinerary( *animals: Animal ) -> Itinerary:
   return ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=list( animals ),
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME )


def Test_Build_TestUnscheduledStopsOnly_ExpectEmptyRoute(
      stub_walk_graph: None ) -> None:
   walk_route = ItineraryWalkRouteBuilder.build(
      _itinerary( UNSCHEDULED_LION ) )

   assert walk_route == ItineraryWalkRouteBuilder.empty()


def Test_Build_TestScheduledAnimal_ExpectRoundTripRoute(
      stub_walk_graph: None ) -> None:
   walk_route = ItineraryWalkRouteBuilder.build(
      _itinerary( SCHEDULED_LION ) )

   assert [ stop.item_key for stop in walk_route.stops ] == [
      ENTRANCE_ITEM_KEY,
      'African Lion||Africa Savanna||Outdoor',
      ENTRANCE_ITEM_KEY,
   ]
   assert len( walk_route.legs ) == 2
   assert walk_route.legs[ 0 ].from_item_key == ENTRANCE_ITEM_KEY
   assert walk_route.legs[ 0 ].to_item_key == 'African Lion||Africa Savanna||Outdoor'
   assert walk_route.legs[ 1 ].from_item_key == 'African Lion||Africa Savanna||Outdoor'
   assert walk_route.legs[ 1 ].to_item_key == ENTRANCE_ITEM_KEY
   assert len( walk_route.points ) == (
      len( walk_route.legs[ 0 ].node_ids )
      + len( walk_route.legs[ 1 ].node_ids )
      - 1
   )
   assert walk_route.points[ 0 ].node_id == walk_route.legs[ 0 ].node_ids[ 0 ]
   assert walk_route.points[ -1 ].node_id == walk_route.legs[ 1 ].node_ids[ -1 ]
   assert all(
      point.x_px >= 0 and point.y_px >= 0
      for point in walk_route.points )


def Test_Build_TestTransitRideGap_ExpectStopsWithoutLeg(
      stub_walk_graph: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   entrance = WalkRouteAnchor(
      schedule_item_kind=ScheduleItemKind.ENTRANCE,
      item_key=ENTRANCE_ITEM_KEY,
      walk_node_ids=[ ENTRANCE_NODE_ID ],
      start_time=ARRIVAL_TIME,
      end_time=ARRIVAL_TIME )
   onboard = WalkRouteAnchor(
      schedule_item_kind=ScheduleItemKind.TRANSPORTATION,
      item_key='Zoomobile||0||Main',
      walk_node_ids=[ LION_WALK_NODE_ID ],
      start_time='10:00 AM',
      end_time='10:00 AM',
      transit_ride_key='Zoomobile||0',
      transit_endpoint=TransitRideEndpoint.ONBOARDING )
   offboard = WalkRouteAnchor(
      schedule_item_kind=ScheduleItemKind.TRANSPORTATION,
      item_key='Zoomobile||0||Canada',
      walk_node_ids=[ LION_WALK_NODE_ID ],
      start_time='10:20 AM',
      end_time='10:20 AM',
      transit_ride_key='Zoomobile||0',
      transit_endpoint=TransitRideEndpoint.OFFBOARDING )
   animal = WalkRouteAnchor(
      schedule_item_kind=ScheduleItemKind.ANIMAL,
      item_key='African Lion||Africa Savanna||Outdoor',
      walk_node_ids=[ LION_WALK_NODE_ID ],
      start_time='10:30 AM',
      end_time='11:00 AM' )

   monkeypatch.setattr(
      WalkRouteAnchorBuilder,
      'build',
      lambda itinerary: [ entrance, onboard, offboard, animal ] )
   monkeypatch.setattr(
      'api.itinerary.routing.itinerary_walk_route_builder.TransitStationRideGapChecker.is_gap',
      lambda previous, nxt: (
         previous.transit_endpoint == TransitRideEndpoint.ONBOARDING
         and nxt.transit_endpoint == TransitRideEndpoint.OFFBOARDING ) )

   walk_route = ItineraryWalkRouteBuilder.build( _itinerary( SCHEDULED_LION ) )

   assert any(
      stop.item_key == 'Zoomobile||0||Canada'
      for stop in walk_route.stops )
   assert all(
      leg.from_item_key != 'Zoomobile||0||Main'
      or leg.to_item_key != 'Zoomobile||0||Canada'
      for leg in walk_route.legs )


def Test_Build_TestUnresolvedAnchorNode_ExpectSkipped(
      stub_walk_graph: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   entrance = WalkRouteAnchor(
      schedule_item_kind=ScheduleItemKind.ENTRANCE,
      item_key=ENTRANCE_ITEM_KEY,
      walk_node_ids=[ ENTRANCE_NODE_ID ],
      start_time=ARRIVAL_TIME,
      end_time=ARRIVAL_TIME )
   empty_anchor = WalkRouteAnchor(
      schedule_item_kind=ScheduleItemKind.ANIMAL,
      item_key='Missing||Exhibit||Outdoor',
      walk_node_ids=[],
      start_time='10:00 AM',
      end_time='10:30 AM' )
   animal = WalkRouteAnchor(
      schedule_item_kind=ScheduleItemKind.ANIMAL,
      item_key='African Lion||Africa Savanna||Outdoor',
      walk_node_ids=[ LION_WALK_NODE_ID ],
      start_time='11:00 AM',
      end_time='11:30 AM' )

   monkeypatch.setattr(
      WalkRouteAnchorBuilder,
      'build',
      lambda itinerary: [ entrance, empty_anchor, animal ] )

   walk_route = ItineraryWalkRouteBuilder.build( _itinerary( SCHEDULED_LION ) )

   assert [ stop.item_key for stop in walk_route.stops ][ :2 ] == [
      ENTRANCE_ITEM_KEY,
      'African Lion||Africa Savanna||Outdoor',
   ]


def Test_Build_TestMissingShortestPath_ExpectEmptyWhenNoLegs(
      stub_walk_graph: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ShortestPathCalculator,
      'find',
      lambda *args, **kwargs: None )

   walk_route = ItineraryWalkRouteBuilder.build( _itinerary( SCHEDULED_LION ) )

   assert walk_route == ItineraryWalkRouteBuilder.empty()


def Test_ResolveWalkRouteAnchorNodeId_TestMultiNodeAnimal_ExpectRepresentative(
      stub_walk_graph: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   def resolve(
         walk_graph: WalkGraph,
         from_node_id: str,
         walk_node_ids: list[ str ] ) -> str:
      captured[ 'from_node_id' ] = from_node_id
      captured[ 'walk_node_ids' ] = list( walk_node_ids )
      return walk_node_ids[ 1 ]

   monkeypatch.setattr( RepresentativeWalkNodeResolver, 'resolve', resolve )

   anchor = WalkRouteAnchor(
      schedule_item_kind=ScheduleItemKind.ANIMAL,
      item_key='African Lion||Africa Savanna||Outdoor',
      walk_node_ids=[ 'n-a', 'n-b' ],
      start_time='10:00 AM',
      end_time='10:30 AM' )

   node_id = ItineraryWalkRouteBuilder._resolve_walk_route_anchor_node_id(
      TEST_GRAPH,
      from_node_id=ENTRANCE_NODE_ID,
      anchor=anchor )

   assert node_id == 'n-b'
   assert captured[ 'walk_node_ids' ] == [ 'n-a', 'n-b' ]


def Test_WalkRoutePointsFromNodeIds_TestMissingNode_ExpectSkipped() -> None:
   points = ItineraryWalkRouteBuilder._walk_route_points_from_node_ids(
      [ ENTRANCE_NODE_ID, 'missing', LION_WALK_NODE_ID ],
      {
         ENTRANCE_NODE_ID: TEST_GRAPH[ 'nodes' ][ 0 ],
         LION_WALK_NODE_ID: TEST_GRAPH[ 'nodes' ][ 1 ],
      } )

   assert [ point.node_id for point in points ] == [
      ENTRANCE_NODE_ID,
      LION_WALK_NODE_ID,
   ]


def Test_ResolveWalkRouteAnchorNodeId_TestMultiNodeNonAnimal_ExpectRepresentative(
      stub_walk_graph: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      RepresentativeWalkNodeResolver,
      'resolve',
      lambda walk_graph, from_node_id, walk_node_ids: walk_node_ids[ 0 ] )

   anchor = WalkRouteAnchor(
      schedule_item_kind=ScheduleItemKind.ATTRACTION,
      item_key='Splash Island',
      walk_node_ids=[ 'n-a', 'n-b' ],
      start_time='10:00 AM',
      end_time='10:30 AM' )

   assert ItineraryWalkRouteBuilder._resolve_walk_route_anchor_node_id(
      TEST_GRAPH,
      from_node_id=ENTRANCE_NODE_ID,
      anchor=anchor ) == 'n-a'
