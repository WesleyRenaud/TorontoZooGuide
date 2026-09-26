from __future__ import annotations

from datetime import date

import pytest

from api.itinerary.data_access.transportation_day_loop_provider import TransportationDayLoopProvider
from api.itinerary.transportation.transportation_day_loop_fetcher import TransportationDayLoopFetcher
from api.itinerary.transportation.transportation_route_leg_orderer import TransportationRouteLegOrderer
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.itinerary.transportation.transportation_route_resolver import TransportationRouteResolver
from api.shared.enums.transportation_name import TransportationName


VISIT_DATE = date( 2026, 6, 15 )
WINTER_VISIT_DATE = date( 2026, 1, 15 )
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
TUNDRA = 'Tundra Zoomobile Station'
EURASIA = 'Eurasia Zoomobile Station'
INDO_MALAYA = 'Indo-Malaya Zoomobile Station'
SUMMER_ROUTE = 'summer'
WINTER_ROUTE = 'winter'

LEG_ROWS = [
   TransportationRouteLegSegment( MAIN, CANADA, 20 ),
   TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
   TransportationRouteLegSegment( AFRICA, MAIN, 45 ),
]


@pytest.fixture
def stub_transportation_day_loop_fetcher( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_main_transportation_station',
      lambda conn, transportation: MAIN if transportation == TransportationName.ZOOMOBILE else None )
   monkeypatch.setattr(
      TransportationRouteResolver,
      'resolve_for_date',
      lambda conn, *, transportation, target_date: SUMMER_ROUTE )
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_route_legs',
      lambda conn, *, transportation, route: LEG_ROWS )


def Test_Fetch_TestOwnedLegRows_ExpectOrderedDayLoop(
      stub_transportation_day_loop_fetcher: None ) -> None:
   day_loop = TransportationDayLoopFetcher.fetch(
      None,
      transportation=TransportationName.ZOOMOBILE,
      target_date=VISIT_DATE )

   assert day_loop is not None
   assert day_loop.transportation == TransportationName.ZOOMOBILE
   assert day_loop.route == SUMMER_ROUTE
   assert day_loop.main_station == MAIN
   assert day_loop.legs == TransportationRouteLegOrderer.order_from_station(
      LEG_ROWS,
      start_station=MAIN )


def Test_Fetch_TestMissingMainStation_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_main_transportation_station',
      lambda conn, transportation: None )

   day_loop = TransportationDayLoopFetcher.fetch(
      None,
      transportation=TransportationName.ZOOMOBILE,
      target_date=VISIT_DATE )

   assert day_loop is None


def Test_Fetch_TestNoLegRows_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_main_transportation_station',
      lambda conn, transportation: MAIN )
   monkeypatch.setattr(
      TransportationRouteResolver,
      'resolve_for_date',
      lambda conn, *, transportation, target_date: SUMMER_ROUTE )
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_route_legs',
      lambda conn, *, transportation, route: [] )

   day_loop = TransportationDayLoopFetcher.fetch(
      None,
      transportation=TransportationName.ZOOMOBILE,
      target_date=VISIT_DATE )

   assert day_loop is None


def Test_Fetch_TestSummerRoute_ExpectSummerStationSequence(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   summer_legs = [
      TransportationRouteLegSegment( MAIN, CANADA, 20 ),
      TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
      TransportationRouteLegSegment( AFRICA, TUNDRA, 15 ),
      TransportationRouteLegSegment( TUNDRA, EURASIA, 15 ),
      TransportationRouteLegSegment( EURASIA, MAIN, 15 ),
   ]
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_main_transportation_station',
      lambda conn, transportation: MAIN )
   monkeypatch.setattr(
      TransportationRouteResolver,
      'resolve_for_date',
      lambda conn, *, transportation, target_date: SUMMER_ROUTE )
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_route_legs',
      lambda conn, *, transportation, route: summer_legs )

   summer_loop = TransportationDayLoopFetcher.fetch(
      None,
      transportation=TransportationName.ZOOMOBILE,
      target_date=VISIT_DATE )

   assert summer_loop is not None
   assert summer_loop.route == SUMMER_ROUTE
   assert summer_loop.main_station == MAIN
   assert summer_loop.legs == TransportationRouteLegOrderer.order_from_station(
      summer_legs,
      start_station=MAIN )


def Test_Fetch_TestWinterRoute_ExpectWinterStationSequence(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   winter_legs = [
      TransportationRouteLegSegment( MAIN, INDO_MALAYA, 10 ),
      TransportationRouteLegSegment( INDO_MALAYA, TUNDRA, 20 ),
      TransportationRouteLegSegment( TUNDRA, EURASIA, 15 ),
      TransportationRouteLegSegment( EURASIA, MAIN, 15 ),
   ]
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_main_transportation_station',
      lambda conn, transportation: MAIN )
   monkeypatch.setattr(
      TransportationRouteResolver,
      'resolve_for_date',
      lambda conn, *, transportation, target_date: WINTER_ROUTE )
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_route_legs',
      lambda conn, *, transportation, route: winter_legs )

   winter_loop = TransportationDayLoopFetcher.fetch(
      None,
      transportation=TransportationName.ZOOMOBILE,
      target_date=WINTER_VISIT_DATE )

   assert winter_loop is not None
   assert winter_loop.route == WINTER_ROUTE
   assert winter_loop.legs == TransportationRouteLegOrderer.order_from_station(
      winter_legs,
      start_station=MAIN )
