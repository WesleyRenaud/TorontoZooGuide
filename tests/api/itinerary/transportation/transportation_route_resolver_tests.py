from __future__ import annotations

from datetime import date

import pytest

from api.itinerary.data_access.transportation_day_loop_provider import TransportationDayLoopProvider
from api.itinerary.transportation.transportation_route_resolver import TransportationRouteResolver
from api.shared.enums.transportation_name import TransportationName


VISIT_DATE = date( 2026, 6, 15 )


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
      if transportation == TransportationName.ZOOMOBILE and month == 6 and day == 15
      else None )


def Test_ResolveForDate_TestSummerDay_ExpectDayRoute(
      stub_transportation_route_resolver: None ) -> None:
   route = TransportationRouteResolver.resolve_for_date(
      None,
      transportation=TransportationName.ZOOMOBILE,
      target_date=VISIT_DATE )

   assert route == 'summer'


def Test_ResolveForDate_TestActiveRouteOverride_ExpectActiveRoute(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   active_route = 'winter'
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_active_route',
      lambda conn, *, transportation, target_date: active_route )
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_day_route',
      lambda conn, *, transportation, month, day: 'summer' )

   route = TransportationRouteResolver.resolve_for_date(
      None,
      transportation=TransportationName.ZOOMOBILE,
      target_date=VISIT_DATE )

   assert route == active_route


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
         transportation=TransportationName.ZOOMOBILE,
         target_date=VISIT_DATE )
