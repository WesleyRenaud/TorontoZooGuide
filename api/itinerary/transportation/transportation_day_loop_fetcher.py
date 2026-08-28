from __future__ import annotations

from datetime import date

from ..data_access.transportation_day_loop_provider import TransportationDayLoopProvider
from .transportation_day_loop import TransportationDayLoop
from .transportation_route_leg_orderer import TransportationRouteLegOrderer
from .transportation_route_resolver import TransportationRouteResolver
from ...types import Types


class TransportationDayLoopFetcher():
   @classmethod
   def fetch(
         cls,
         conn: Types.Connection,
         *,
         transportation: str,
         target_date: date ) -> TransportationDayLoop | None:
      main_station = TransportationDayLoopProvider.fetch_main_transportation_station(
         conn,
         transportation )

      if main_station is None:
         return None

      route = TransportationRouteResolver.resolve_for_date(
         conn,
         transportation=transportation,
         target_date=target_date )
      leg_rows = TransportationDayLoopProvider.fetch_transportation_route_legs(
         conn,
         transportation=transportation,
         route=route )

      if not leg_rows:
         return None

      return TransportationDayLoop(
         transportation=transportation,
         route=route,
         main_station=main_station,
         legs=TransportationRouteLegOrderer.order_from_station(
            leg_rows,
            start_station=main_station ) )
