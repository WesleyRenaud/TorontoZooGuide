from __future__ import annotations

from ...models import ZoomobileStation
from ...models.zoomobile_route import ZoomobileRoute
from ...shared.calendar_dates import CalendarDates
from ...shared.enums.zoomobile_route import ZoomobileRouteId
from ...shared.enums.zoomobile_route import ZoomobileRouteSource
from ...types import MonthInput, VisitDay, VisitYear
from .zoomobile_route_context import ZoomobileRouteContext


def is_valid_zoomobile_route( route: str | None ) -> bool:
   if route is None:
      return False

   try:
      ZoomobileRouteId( route )
      return True
   except ValueError:
      return False


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
      day_route: str | None ) -> tuple[ str, str ]:

   if requested_route in (
         ZoomobileRouteId.SUMMER.value,
         ZoomobileRouteId.WINTER.value,
   ):
      return requested_route, ZoomobileRouteSource.MANUAL.value

   return resolve_zoomobile_route(
      requested_route,
      active_route,
      day_route )


def resolve_zoomobile_route(
      requested_route: str,
      active_route: str | None,
      day_route: str | None ) -> tuple[ str, str ]:

   route = requested_route
   route_source = ZoomobileRouteSource.MANUAL

   if route == 'current':
      route = active_route

      if is_valid_zoomobile_route( route ):
         route_source = ZoomobileRouteSource.OVERRIDE
      else:
         route = day_route
         route_source = ZoomobileRouteSource.FALLBACK

   if not is_valid_zoomobile_route( route ):
      route = ZoomobileRouteId.SUMMER.value

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
