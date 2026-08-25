from __future__ import annotations

from .active_transportation_route_context import TransportationRouteContext
from ...models import TransportationStation
from ...models.active_transportation_route import ActiveTransportationRoute
from ...shared.calendar_dates import CalendarDates
from ...shared.enums.transportation_route import TransportationRouteId
from ...shared.enums.transportation_route import TransportationRouteSource
from ...types import MonthInput, VisitDay, VisitYear


def is_valid_transportation_route(
      route: str | None,
      valid_routes: list[ str ] ) -> bool:
   return route is not None and route in valid_routes


def resolve_transportation_route_context(
      day: VisitDay,
      month: MonthInput,
      year: VisitYear ) -> TransportationRouteContext:
   target_date = CalendarDates.visit_target_date(
      month=month,
      day=day,
      year=year )

   return TransportationRouteContext(
      normalized_month=target_date.month,
      normalized_day=target_date.day,
      target_date=target_date,
   )


def resolve_requested_transportation_route(
      requested_route: str,
      active_route: str | None,
      day_route: str | None,
      valid_routes: list[ str ] ) -> tuple[ str, str ]:

   if is_valid_transportation_route( requested_route, valid_routes ):
      return requested_route, TransportationRouteSource.MANUAL.value

   return resolve_transportation_route(
      requested_route,
      active_route,
      day_route,
      valid_routes )


def resolve_transportation_route(
      requested_route: str,
      active_route: str | None,
      day_route: str | None,
      valid_routes: list[ str ] ) -> tuple[ str, str ]:

   route = requested_route
   route_source = TransportationRouteSource.MANUAL

   if route == 'current':
      route = active_route

      if is_valid_transportation_route( route, valid_routes ):
         route_source = TransportationRouteSource.OVERRIDE
      else:
         route = day_route
         route_source = TransportationRouteSource.FALLBACK

   if not is_valid_transportation_route( route, valid_routes ):
      route = (
         TransportationRouteId.SUMMER.value
         if TransportationRouteId.SUMMER.value in valid_routes
         else valid_routes[ 0 ] if valid_routes else TransportationRouteId.SUMMER.value
      )

   return route, route_source.value


def build_active_transportation_route_response(
      route: str,
      route_source: str,
      transportation_stations: list[ TransportationStation ] ) -> ActiveTransportationRoute:

   return ActiveTransportationRoute(
      route=route,
      route_source=route_source,
      transportation_stations=transportation_stations,
   )
