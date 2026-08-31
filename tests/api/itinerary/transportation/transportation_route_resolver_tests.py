from __future__ import annotations

from datetime import date

import pytest

from api.itinerary.data_access.transportation_day_loop_provider import TransportationDayLoopProvider
from api.itinerary.transportation.transportation_route_resolver import TransportationRouteResolver


VISIT_DATE = date( 2026, 6, 15 )
ZOOMOBILE = 'Zoomobile'


@pytest.fixture
def stub_transportation_route_resolver( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_active_route',
      lambda conn, *, transportation, target_date: None )
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_day_route',
      lambda conn, *, transportation, month, day: 'summer'
      if transportation == ZOOMOBILE and month == 6 and day == 15
      else None )


def Test_ResolveForDate_TestSummerDay_ExpectDayRoute(
      stub_transportation_route_resolver: None ) -> None:
   assert TransportationRouteResolver.resolve_for_date(
      None,
      transportation=ZOOMOBILE,
      target_date=VISIT_DATE ) == 'summer'


def Test_ResolveForDate_TestActiveRouteOverride_ExpectActiveRoute(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_active_route',
      lambda conn, *, transportation, target_date: 'winter' )
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_day_route',
      lambda conn, *, transportation, month, day: 'summer' )

   assert TransportationRouteResolver.resolve_for_date(
      None,
      transportation=ZOOMOBILE,
      target_date=VISIT_DATE ) == 'winter'


def Test_ResolveForDate_TestMissingRoute_ExpectValueError(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_active_route',
      lambda conn, *, transportation, target_date: None )
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_day_route',
      lambda conn, *, transportation, month, day: None )

   with pytest.raises( ValueError, match='No route defined' ):
      TransportationRouteResolver.resolve_for_date(
         None,
         transportation=ZOOMOBILE,
         target_date=VISIT_DATE )
