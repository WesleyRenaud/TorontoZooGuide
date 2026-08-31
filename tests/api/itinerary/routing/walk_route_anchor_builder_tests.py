from __future__ import annotations

import pytest

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.routing.itinerary_stop import ENTRANCE_ITEM_KEY
from api.itinerary.routing.transit_ride_endpoint import TransitRideEndpoint
from api.itinerary.routing.transportation_station_walk_node_resolver import TransportationStationWalkNodeResolver
from api.itinerary.routing.walk_route_anchor_builder import WalkRouteAnchorBuilder
from api.models import Animal
from api.models import Itinerary
from api.models.itinerary_transportation import ItineraryTransportation
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.enums import ScheduleItemKind
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode
from api.walk_graph.viewing_walk_node_id_resolver import ViewingWalkNodeIdResolver


VISIT_DATE = '2026-06-20'
ARRIVAL_TIME = '9:30 AM'
DEPARTURE_TIME = '5:00 PM'

ZOOMOBILE = 'Zoomobile'
MAIN_STATION = 'Main Zoomobile Station'
CANADA_STATION = 'Canadian Domain Zoomobile Station'

ENTRANCE_NODE_ID = 'n-1'
LION_WALK_NODE_ID = 'n-2001'
ONBOARD_NODE_ID = 'n-onboard'
OFFBOARD_NODE_ID = 'n-offboard'

UNSCHEDULED_LION = Animal(
   species='African Lion',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
   enclosure_type='Outdoor',
   x_coord=50.0,
   y_coord=60.0,
)

SCHEDULED_LION = Animal(
   species='African Lion',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
   enclosure_type='Outdoor',
   x_coord=50.0,
   y_coord=60.0,
   start_time='10:00 AM',
   end_time='10:30 AM',
)

ZOOMOBILE_LEGS = [
   ItineraryTransportationLeg(
      MAIN_STATION,
      CANADA_STATION,
      '10:00 AM',
      '10:20 AM',
      ZOOMOBILE,
      False ),
]

STATION_NODE_IDS = {
   MAIN_STATION: ONBOARD_NODE_ID,
   CANADA_STATION: OFFBOARD_NODE_ID,
}


def _node( node_id: str, x: float, y: float ) -> WalkGraphNode:
   return {
      'id': node_id,
      'x': x,
      'y': y,
      'x_px': x,
      'y_px': y,
   }


TEST_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': ENTRANCE_NODE_ID,
   'nodes': [
      _node( ENTRANCE_NODE_ID, 61.414, 91.366 ),
      _node( LION_WALK_NODE_ID, 50.0, 60.0 ),
   ],
   'edges': [],
}


def _clear_walk_graph_provider_cache() -> None:
   WalkGraphProvider.fetch.cache_clear()


def _itinerary(
      *,
      animals: list[ Animal ] | None = None,
      transportations: list[ ItineraryTransportation ] | None = None ) -> Itinerary:
   return ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=animals or [],
      attractions=[],
      transportations=transportations or [],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME )


def _resolve_station_node( transportation_name: str, station_name: str ) -> str | None:
   return STATION_NODE_IDS.get( station_name )


@pytest.fixture
def stub_walk_route_anchor_dependencies( monkeypatch: pytest.MonkeyPatch ) -> None:
   _clear_walk_graph_provider_cache()
   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: TEST_GRAPH )
   monkeypatch.setattr(
      ViewingWalkNodeIdResolver,
      'resolve',
      lambda *args, **kwargs: LION_WALK_NODE_ID )
   monkeypatch.setattr(
      TransportationStationWalkNodeResolver,
      'resolve',
      _resolve_station_node )
   yield


def Test_Build_TestUnscheduledAnimal_ExpectEmpty(
      stub_walk_route_anchor_dependencies: None ) -> None:
   assert WalkRouteAnchorBuilder.build(
      _itinerary( animals=[ UNSCHEDULED_LION ] ) ) == []


def Test_Build_TestScheduledAnimal_ExpectEntranceAndAnimalAnchors(
      stub_walk_route_anchor_dependencies: None ) -> None:
   anchors = WalkRouteAnchorBuilder.build(
      _itinerary( animals=[ SCHEDULED_LION ] ) )

   assert len( anchors ) == 2
   assert anchors[ 0 ].schedule_item_kind == ScheduleItemKind.ENTRANCE
   assert anchors[ 0 ].item_key == ENTRANCE_ITEM_KEY
   assert anchors[ 0 ].walk_node_ids == [ ENTRANCE_NODE_ID ]
   assert anchors[ 1 ].schedule_item_kind == ScheduleItemKind.ANIMAL
   assert anchors[ 1 ].item_key == 'African Lion||Africa Savanna||Outdoor'
   assert anchors[ 1 ].walk_node_ids == [ LION_WALK_NODE_ID ]
   assert anchors[ 1 ].start_time == '10:00 AM'


def Test_Build_TestTransitRide_ExpectOnboardAndOffboardAnchors(
      stub_walk_route_anchor_dependencies: None ) -> None:
   anchors = WalkRouteAnchorBuilder.build(
      _itinerary(
         transportations=[
            ItineraryTransportation(
               name=ZOOMOBILE,
               added_as_attraction=False,
               legs=ZOOMOBILE_LEGS ),
         ] ) )

   assert len( anchors ) == 3
   assert anchors[ 0 ].schedule_item_kind == ScheduleItemKind.ENTRANCE

   onboarding_anchor = anchors[ 1 ]
   offboarding_anchor = anchors[ 2 ]

   assert onboarding_anchor.transit_endpoint == TransitRideEndpoint.ONBOARDING
   assert onboarding_anchor.walk_node_ids == [ ONBOARD_NODE_ID ]
   assert onboarding_anchor.start_time == '10:00 AM'
   assert offboarding_anchor.transit_endpoint == TransitRideEndpoint.OFFBOARDING
   assert offboarding_anchor.walk_node_ids == [ OFFBOARD_NODE_ID ]
   assert offboarding_anchor.start_time == '10:20 AM'
