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


def Test_ResolveForDate_TestSummerDay_ExpectMonthRoute(
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

   route = TransportationRouteResolver.resolve_for_date(
      None,
      transportation=TransportationName.ZOOMOBILE,
      target_date=VISIT_DATE )

   assert route == active_route


def Test_ResolveForDate_TestOtherTransportation_ExpectValueError(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationDayLoopProvider,
      'fetch_transportation_active_route',
      lambda conn, *, transportation, target_date: None )

   with pytest.raises( ValueError, match='No route defined' ):
      TransportationRouteResolver.resolve_for_date(
         None,
         transportation='Tundra Trek Ride',
         target_date=VISIT_DATE )
