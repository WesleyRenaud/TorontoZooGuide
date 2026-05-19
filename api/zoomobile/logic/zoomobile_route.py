from ... import zoo
from ...models.zoomobile_route import ZoomobileRoute
from ...shared.enums.zoomobile_route import ZoomobileRouteId
from ...shared.enums.zoomobile_route import ZoomobileRouteSource
from .zoomobile_route_context import ZoomobileRouteContext


def is_valid_zoomobile_route( route ):
   if route is None:
      return False

   try:
      ZoomobileRouteId( route )
      return True
   except ValueError:
      return False


def resolve_zoomobile_route_context( day, month, year ):
   target_date = zoo.ZooUtil.visit_target_date(
      month=month,
      day=day,
      year=year )

   return ZoomobileRouteContext(
      normalized_month=target_date.month,
      normalized_day=target_date.day,
      target_date=target_date,
   )


def resolve_zoomobile_route(
      requested_route,
      active_route,
      day_route ):

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
      route,
      route_source,
      zoomobile_stations ):

   return ZoomobileRoute(
      route=route,
      route_source=route_source,
      zoomobile_stations=tuple( zoomobile_stations ),
   )
