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


ZOOMOBILE = 'Zoomobile'
MAIN_STATION = 'Main Zoomobile Station'
CANADA_STATION = 'Canadian Domain Zoomobile Station'
EURASIA_STATION = 'Eurasia Zoomobile Station'

ONBOARD_NODE_ID = 'n-onboard'
OFFBOARD_NODE_ID = 'n-offboard'
DEFAULT_BOARDING_NODE_ID = 'n-default'

TRANSPORTATION_LEGS = [
   ItineraryTransportationLeg(
      MAIN_STATION,
      CANADA_STATION,
      '10:00 AM',
      '10:20 AM',
      ZOOMOBILE,
      False ),
   ItineraryTransportationLeg(
      CANADA_STATION,
      EURASIA_STATION,
      '10:20 AM',
      '10:30 AM',
      ZOOMOBILE,
      False ),
]

STATION_NODE_IDS = {
   MAIN_STATION: ONBOARD_NODE_ID,
   EURASIA_STATION: OFFBOARD_NODE_ID,
}


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
   assert TransportationWalkNodeResolver.resolve(
      ZOOMOBILE,
      legs=TRANSPORTATION_LEGS,
      endpoint=TransitRideEndpoint.ONBOARDING ) == ONBOARD_NODE_ID


def Test_Resolve_TestOffboardingLegs_ExpectLastStationWalkNode(
      stub_transportation_walk_node_dependencies: None ) -> None:
   assert TransportationWalkNodeResolver.resolve(
      ZOOMOBILE,
      legs=TRANSPORTATION_LEGS,
      endpoint=TransitRideEndpoint.OFFBOARDING ) == OFFBOARD_NODE_ID


def Test_Resolve_TestNoConnection_ExpectNone( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: None )

   assert TransportationWalkNodeResolver.resolve( ZOOMOBILE ) is None


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

   assert TransportationWalkNodeResolver.resolve( ZOOMOBILE ) == DEFAULT_BOARDING_NODE_ID


def Test_Resolve_TestDayLoopLegs_ExpectFirstFromStation(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   class _DayLoop:
      legs = TRANSPORTATION_LEGS

   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: object() )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_itinerary_date_record',
      lambda conn: type( 'DateRecord', (), { 'itinerary_date': '2026-06-20' } )() )
   monkeypatch.setattr(
      TransportationDayLoopFetcher,
      'fetch',
      lambda conn, *, transportation, target_date: _DayLoop() )
   monkeypatch.setattr(
      TransportationStationWalkNodeResolver,
      'resolve',
      _resolve_station_node )

   assert TransportationWalkNodeResolver.resolve( ZOOMOBILE ) == ONBOARD_NODE_ID
