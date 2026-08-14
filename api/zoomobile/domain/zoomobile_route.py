from __future__ import annotations

from ...models import ZoomobileStation
from ...models.zoomobile_route import ZoomobileRoute
from ...shared.calendar_dates import CalendarDates
from ...shared.enums.zoomobile_route import ZoomobileRouteId
from ...shared.enums.zoomobile_route import ZoomobileRouteSource
from ...types import MonthInput, VisitDay, VisitYear
from .zoomobile_route_context import ZoomobileRouteContext


def is_valid_zoomobile_route(
      route: str | None,
      valid_routes: list[ str ] ) -> bool:
   return route is not None and route in valid_routes


def resolve_zoomobile_route_context(
      day: VisitDay,
      month: MonthInput,
      year: VisitYear ) -> ZoomobileRouteContext:
   target_date = CalendarDates.visit_target_date(
      month=month,
      day=day,
      year=year )

   return ZoomobileRouteContext(
      normalized_month=target_date.month,
      normalized_day=target_date.day,
      target_date=target_date,
   )


def resolve_requested_zoomobile_route(
      requested_route: str,
      active_route: str | None,
      day_route: str | None,
      valid_routes: list[ str ] ) -> tuple[ str, str ]:

   if is_valid_zoomobile_route( requested_route, valid_routes ):
      return requested_route, ZoomobileRouteSource.MANUAL.value

   return resolve_zoomobile_route(
      requested_route,
      active_route,
      day_route,
      valid_routes )


def resolve_zoomobile_route(
      requested_route: str,
      active_route: str | None,
      day_route: str | None,
      valid_routes: list[ str ] ) -> tuple[ str, str ]:

   route = requested_route
   route_source = ZoomobileRouteSource.MANUAL

   if route == 'current':
      route = active_route

      if is_valid_zoomobile_route( route, valid_routes ):
         route_source = ZoomobileRouteSource.OVERRIDE
      else:
         route = day_route
         route_source = ZoomobileRouteSource.FALLBACK

   if not is_valid_zoomobile_route( route, valid_routes ):
      route = (
         ZoomobileRouteId.SUMMER.value
         if ZoomobileRouteId.SUMMER.value in valid_routes
         else valid_routes[ 0 ] if valid_routes else ZoomobileRouteId.SUMMER.value
      )

   return route, route_source.value


def build_zoomobile_route_response(
      route: str,
      route_source: str,
      zoomobile_stations: list[ ZoomobileStation ] ) -> ZoomobileRoute:

   return ZoomobileRoute(
      route=route,
      route_source=route_source,
      zoomobile_stations=zoomobile_stations,
   )
