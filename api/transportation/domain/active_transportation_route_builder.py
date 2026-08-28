from __future__ import annotations

from ...models import TransportationStation
from ...models.active_transportation_route import ActiveTransportationRoute
from ...shared.calendar_dates import CalendarDates
from ...shared.enums.transportation_route_id import TransportationRouteId
from ...shared.enums.transportation_route_source import TransportationRouteSource
from .transportation_route_context import TransportationRouteContext
from ...types import Types


class ActiveTransportationRouteBuilder():
   @classmethod
   def is_valid_transportation_route(
         cls,
         route: str | None,
         valid_routes: list[ str ] ) -> bool:
      return route is not None and route in valid_routes


   @classmethod
   def resolve_transportation_route_context(
         cls,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear ) -> TransportationRouteContext:
      target_date = CalendarDates.visit_target_date(
         month=month,
         day=day,
         year=year )
      return TransportationRouteContext(
         normalized_month=target_date.month,
         normalized_day=target_date.day,
         target_date=target_date,
      )


   @classmethod
   def resolve_requested_transportation_route(
         cls,
         requested_route: str,
         active_route: str | None,
         day_route: str | None,
         valid_routes: list[ str ] ) -> tuple[ str, str ]:
      if cls.is_valid_transportation_route( requested_route, valid_routes ):
         return requested_route, TransportationRouteSource.MANUAL.value
      return cls.resolve_transportation_route(
         requested_route,
         active_route,
         day_route,
         valid_routes )


   @classmethod
   def resolve_transportation_route(
         cls,
         requested_route: str,
         active_route: str | None,
         day_route: str | None,
         valid_routes: list[ str ] ) -> tuple[ str, str ]:
      route = requested_route
      route_source = TransportationRouteSource.MANUAL

      if route == 'current':
         route = active_route
         if cls.is_valid_transportation_route( route, valid_routes ):
            route_source = TransportationRouteSource.OVERRIDE
         else:
            route = day_route
            route_source = TransportationRouteSource.FALLBACK

      if not cls.is_valid_transportation_route( route, valid_routes ):
         route = (
            TransportationRouteId.SUMMER.value
            if TransportationRouteId.SUMMER.value in valid_routes
            else valid_routes[ 0 ] if valid_routes else TransportationRouteId.SUMMER.value
         )

      return route, route_source.value


   @classmethod
   def build_active_transportation_route_response(
         cls,
         route: str,
         route_source: str,
         transportation_stations: list[ TransportationStation ] ) -> ActiveTransportationRoute:
      return ActiveTransportationRoute(
         route=route,
         route_source=route_source,
         transportation_stations=transportation_stations,
      )
