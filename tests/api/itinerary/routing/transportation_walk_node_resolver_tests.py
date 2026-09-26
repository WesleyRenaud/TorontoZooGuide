from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.data_access.transportation_day_loop_provider import TransportationDayLoopProvider
from api.itinerary.routing.transit_ride_endpoint import TransitRideEndpoint
from api.itinerary.routing.transportation_station_walk_node_resolver import TransportationStationWalkNodeResolver
from api.itinerary.routing.transportation_walk_node_resolver import TransportationWalkNodeResolver
from api.itinerary.transportation.transportation_day_loop_fetcher import TransportationDayLoopFetcher
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.request_connection_provider import RequestConnectionProvider
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName


MAIN_STATION = 'Main Zoomobile Station'
CANADA_STATION = 'Canadian Domain Zoomobile Station'
EURASIA_STATION = 'Eurasia Zoomobile Station'
ONBOARD_NODE_ID = 'n-onboard'
OFFBOARD_NODE_ID = 'n-offboard'
DEFAULT_BOARDING_NODE_ID = 'n-default'
VISIT_DATE = '2026-06-20'

TRANSPORTATION_LEGS = [
   ItineraryTransportationLeg(
      MAIN_STATION,
      CANADA_STATION,
      '10:00 AM',
      '10:20 AM',
      TransportationName.ZOOMOBILE,
      False ),
   ItineraryTransportationLeg(
      CANADA_STATION,
      EURASIA_STATION,
      '10:20 AM',
      '10:30 AM',
      TransportationName.ZOOMOBILE,
      False ),
]

STATION_NODE_IDS = {
   MAIN_STATION: ONBOARD_NODE_ID,
   EURASIA_STATION: OFFBOARD_NODE_ID,
}


class _ItineraryDateRecord:
   itinerary_date = VISIT_DATE


class _DayLoop:
   legs = TRANSPORTATION_LEGS


def _resolve_station_node( transportation_name: str, station_name: str ) -> str | None:
   return STATION_NODE_IDS.get( station_name )


@pytest.fixture
def stub_transportation_walk_node_dependencies( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationStationWalkNodeResolver,
      'resolve',
      _resolve_station_node )


def Test_Resolve_TestOnboardingLegs_ExpectFirstStationWalkNode(
      stub_transportation_walk_node_dependencies: None ) -> None:
   onboarding_station = TRANSPORTATION_LEGS[ Position.FIRST ].from_station

   walk_node_id = TransportationWalkNodeResolver.resolve(
      TransportationName.ZOOMOBILE,
      legs=TRANSPORTATION_LEGS,
      endpoint=TransitRideEndpoint.ONBOARDING )

   assert walk_node_id == STATION_NODE_IDS[ onboarding_station ]


def Test_Resolve_TestOffboardingLegs_ExpectLastStationWalkNode(
      stub_transportation_walk_node_dependencies: None ) -> None:
   offboarding_station = TRANSPORTATION_LEGS[ Position.LAST ].to_station

   walk_node_id = TransportationWalkNodeResolver.resolve(
      TransportationName.ZOOMOBILE,
      legs=TRANSPORTATION_LEGS,
      endpoint=TransitRideEndpoint.OFFBOARDING )

   assert walk_node_id == STATION_NODE_IDS[ offboarding_station ]


def Test_Resolve_TestNoConnection_ExpectNone( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: None )

   walk_node_id = TransportationWalkNodeResolver.resolve( TransportationName.ZOOMOBILE )

   assert walk_node_id is None


def Test_Resolve_TestDefaultBoardingStation_ExpectMainStationWalkNode(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: object() )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date_record',
      lambda conn: None )
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_main_transportation_station',
      lambda conn, transportation: MAIN_STATION )
   monkeypatch.setattr(
      TransportationStationWalkNodeResolver,
      'resolve',
      lambda transportation_name, station_name: DEFAULT_BOARDING_NODE_ID )

   walk_node_id = TransportationWalkNodeResolver.resolve( TransportationName.ZOOMOBILE )

   assert walk_node_id == DEFAULT_BOARDING_NODE_ID


def Test_Resolve_TestDayLoopLegs_ExpectFirstFromStation(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: object() )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date_record',
      lambda conn: _ItineraryDateRecord() )
   monkeypatch.setattr(
      TransportationDayLoopFetcher,
      'fetch',
      lambda conn, *, transportation, target_date: _DayLoop() )
   monkeypatch.setattr(
      TransportationStationWalkNodeResolver,
      'resolve',
      _resolve_station_node )
   onboarding_station = TRANSPORTATION_LEGS[ Position.FIRST ].from_station

   walk_node_id = TransportationWalkNodeResolver.resolve( TransportationName.ZOOMOBILE )

   assert walk_node_id == STATION_NODE_IDS[ onboarding_station ]
