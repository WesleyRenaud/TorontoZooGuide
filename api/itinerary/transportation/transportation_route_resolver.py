from __future__ import annotations

from datetime import date

from ..data_access.transportation_day_loop_provider import TransportationDayLoopProvider
from ...types import Types


class TransportationRouteResolver():
   @classmethod
   def resolve_for_date(
         cls,
         conn: Types.Connection,
         *,
         transportation: str,
         target_date: date ) -> str:
      active_route = TransportationDayLoopProvider.fetch_transportation_active_route(
         conn,
         transportation=transportation,
         target_date=target_date )

      if active_route is not None:
         return active_route

      day_route = TransportationDayLoopProvider.fetch_transportation_day_route(
         conn,
         transportation=transportation,
         month=target_date.month,
         day=target_date.day )

      if day_route is None:
         raise ValueError(
            f'No route defined for transportation { repr( transportation ) } '
            f'on { target_date.isoformat() }' )

      return day_route
