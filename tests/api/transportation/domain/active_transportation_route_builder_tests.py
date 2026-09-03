from __future__ import annotations

from datetime import date

from api.models.transportation_station import TransportationStation
from api.shared.enums.transportation_route_id import TransportationRouteId
from api.shared.enums.transportation_route_source import TransportationRouteSource
from api.transportation.domain.active_transportation_route_builder import ActiveTransportationRouteBuilder


VALID_ROUTES = [
   TransportationRouteId.SUMMER.value,
   TransportationRouteId.WINTER.value,
]
STATION_COORD = 0.0
VISIT_MONTH = 6
VISIT_DAY = 15
VISIT_YEAR = 2026


def _station( name: str ) -> TransportationStation:
   return TransportationStation(
      name=name,
      description=f'{ name } stop',
      x_coord=STATION_COORD,
      y_coord=STATION_COORD )


def Test_ResolveRequestedTransportationRoute_TestValidManualRoute_ExpectManualSource() -> None:
   route, route_source = ActiveTransportationRouteBuilder.resolve_requested_transportation_route(
      requested_route=TransportationRouteId.WINTER.value,
      active_route=TransportationRouteId.SUMMER.value,
      day_route=TransportationRouteId.SUMMER.value,
      valid_routes=VALID_ROUTES )

   assert route == TransportationRouteId.WINTER.value
   assert route_source == TransportationRouteSource.MANUAL.value


def Test_ResolveTransportationRoute_TestCurrentWithActiveRoute_ExpectOverrideSource() -> None:
   route, route_source = ActiveTransportationRouteBuilder.resolve_transportation_route(
      requested_route='current',
      active_route=TransportationRouteId.WINTER.value,
      day_route=TransportationRouteId.SUMMER.value,
      valid_routes=VALID_ROUTES )

   assert route == TransportationRouteId.WINTER.value
   assert route_source == TransportationRouteSource.OVERRIDE.value


def Test_ResolveTransportationRoute_TestCurrentWithoutActiveRoute_ExpectFallbackSource() -> None:
   route, route_source = ActiveTransportationRouteBuilder.resolve_transportation_route(
      requested_route='current',
      active_route=None,
      day_route=TransportationRouteId.WINTER.value,
      valid_routes=VALID_ROUTES )

   assert route == TransportationRouteId.WINTER.value
   assert route_source == TransportationRouteSource.FALLBACK.value


def Test_ResolveTransportationRoute_TestInvalidRoute_ExpectSummerDefault() -> None:
   route, route_source = ActiveTransportationRouteBuilder.resolve_transportation_route(
      requested_route='invalid-route',
      active_route=None,
      day_route=None,
      valid_routes=VALID_ROUTES )

   assert route == TransportationRouteId.SUMMER.value
   assert route_source == TransportationRouteSource.MANUAL.value


def Test_ResolveTransportationRouteContext_TestVisitDate_ExpectNormalizedContext() -> None:
   context = ActiveTransportationRouteBuilder.resolve_transportation_route_context(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR )

   assert context.target_date == date( VISIT_YEAR, VISIT_MONTH, VISIT_DAY )
   assert context.normalized_month == VISIT_MONTH
   assert context.normalized_day == VISIT_DAY


def Test_BuildActiveTransportationRouteResponse_TestRouteAndStations_ExpectResponseModel() -> None:
   stations = [ _station( 'Africa Station' ) ]

   response = ActiveTransportationRouteBuilder.build_active_transportation_route_response(
      route=TransportationRouteId.SUMMER.value,
      route_source=TransportationRouteSource.MANUAL.value,
      transportation_stations=stations )

   assert response.route == TransportationRouteId.SUMMER.value
   assert response.route_source == TransportationRouteSource.MANUAL.value
   assert response.transportation_stations == stations


def Test_ResolveRequestedTransportationRoute_TestInvalidManualRoute_ExpectFallbackResolution() -> None:
   route, source = ActiveTransportationRouteBuilder.resolve_requested_transportation_route(
      'invalid',
      active_route='summer',
      day_route='summer',
      valid_routes=[ 'summer', 'winter' ],
   )

   assert route == 'summer'
   assert source == TransportationRouteSource.MANUAL.value
