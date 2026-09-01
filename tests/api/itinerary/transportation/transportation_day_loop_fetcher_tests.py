from __future__ import annotations

from datetime import date

import pytest

from api.itinerary.data_access.transportation_day_loop_provider import TransportationDayLoopProvider
from api.itinerary.transportation.transportation_day_loop_fetcher import TransportationDayLoopFetcher
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.itinerary.transportation.transportation_route_resolver import TransportationRouteResolver


VISIT_DATE = date( 2026, 6, 15 )
WINTER_VISIT_DATE = date( 2026, 1, 15 )
ZOOMOBILE = 'Zoomobile'
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'

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
      lambda conn, transportation: MAIN if transportation == ZOOMOBILE else None )
   monkeypatch.setattr(
      TransportationRouteResolver,
      'resolve_for_date',
      lambda conn, *, transportation, target_date: 'summer' )
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_route_legs',
      lambda conn, *, transportation, route: LEG_ROWS )


def Test_Fetch_TestOwnedLegRows_ExpectOrderedDayLoop(
      stub_transportation_day_loop_fetcher: None ) -> None:
   day_loop = TransportationDayLoopFetcher.fetch(
      None,
      transportation=ZOOMOBILE,
      target_date=VISIT_DATE )

   assert day_loop is not None
   assert day_loop.transportation == ZOOMOBILE
   assert day_loop.route == 'summer'
   assert day_loop.main_station == MAIN
   assert [
      ( leg.from_station, leg.to_station, leg.duration_minutes )
      for leg in day_loop.legs
   ] == [
      ( MAIN, CANADA, 20 ),
      ( CANADA, AFRICA, 10 ),
      ( AFRICA, MAIN, 45 ),
   ]


def Test_Fetch_TestMissingMainStation_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_main_transportation_station',
      lambda conn, transportation: None )

   assert TransportationDayLoopFetcher.fetch(
      None,
      transportation=ZOOMOBILE,
      target_date=VISIT_DATE ) is None


def Test_Fetch_TestNoLegRows_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_main_transportation_station',
      lambda conn, transportation: MAIN )
   monkeypatch.setattr(
      TransportationRouteResolver,
      'resolve_for_date',
      lambda conn, *, transportation, target_date: 'summer' )
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_route_legs',
      lambda conn, *, transportation, route: [] )

   assert TransportationDayLoopFetcher.fetch(
      None,
      transportation=ZOOMOBILE,
      target_date=VISIT_DATE ) is None


def Test_Fetch_TestSummerAndWinterRoutes_ExpectDistinctStationSequences(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   summer_legs = [
      TransportationRouteLegSegment( MAIN, CANADA, 20 ),
      TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
      TransportationRouteLegSegment( AFRICA, 'Tundra Zoomobile Station', 15 ),
      TransportationRouteLegSegment( 'Tundra Zoomobile Station', 'Eurasia Zoomobile Station', 15 ),
      TransportationRouteLegSegment( 'Eurasia Zoomobile Station', MAIN, 15 ),
   ]
   winter_legs = [
      TransportationRouteLegSegment( MAIN, 'Indo-Malaya Zoomobile Station', 10 ),
      TransportationRouteLegSegment( 'Indo-Malaya Zoomobile Station', 'Tundra Zoomobile Station', 20 ),
      TransportationRouteLegSegment( 'Tundra Zoomobile Station', 'Eurasia Zoomobile Station', 15 ),
      TransportationRouteLegSegment( 'Eurasia Zoomobile Station', MAIN, 15 ),
   ]

   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_main_transportation_station',
      lambda conn, transportation: MAIN )
   monkeypatch.setattr(
      TransportationRouteResolver,
      'resolve_for_date',
      lambda conn, *, transportation, target_date: (
         'winter' if target_date.month == 1 else 'summer'
      ) )
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_route_legs',
      lambda conn, *, transportation, route: (
         winter_legs if route == 'winter' else summer_legs
      ) )

   summer_loop = TransportationDayLoopFetcher.fetch(
      None,
      transportation=ZOOMOBILE,
      target_date=VISIT_DATE )
   winter_loop = TransportationDayLoopFetcher.fetch(
      None,
      transportation=ZOOMOBILE,
      target_date=WINTER_VISIT_DATE )

   assert summer_loop is not None
   assert summer_loop.route == 'summer'
   assert summer_loop.main_station == MAIN
   assert [
      ( leg.from_station, leg.to_station )
      for leg in summer_loop.legs
   ] == [
      ( leg.from_station, leg.to_station )
      for leg in summer_legs
   ]

   assert winter_loop is not None
   assert winter_loop.route == 'winter'
   assert [
      ( leg.from_station, leg.to_station )
      for leg in winter_loop.legs
   ] == [
      ( leg.from_station, leg.to_station )
      for leg in winter_legs
   ]
