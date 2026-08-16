from __future__ import annotations

from datetime import date

from ..data_access.transportation_day_loop import fetch_main_transportation_station
from ..data_access.transportation_day_loop import fetch_transportation_active_route
from ..data_access.transportation_day_loop import fetch_transportation_day_route
from ..data_access.transportation_day_loop import fetch_transportation_route_legs
from .transportation_day_loop import TransportationDayLoop
from .transportation_route_leg_segment import TransportationRouteLegSegment
from ...types import Connection


def resolve_transportation_route_for_date(
      conn: Connection,
      *,
      transportation: str,
      target_date: date ) -> str:
   active_route = fetch_transportation_active_route(
      conn,
      transportation=transportation,
      target_date=target_date )

   if active_route is not None:
      return active_route

   day_route = fetch_transportation_day_route(
      conn,
      transportation=transportation,
      month=target_date.month,
      day=target_date.day )

   if day_route is None:
      raise ValueError(
         f'No route defined for transportation { repr( transportation ) } '
         f'on { target_date.isoformat() }' )

   return day_route


def order_route_legs_from_station(
      legs: list[ TransportationRouteLegSegment ],
      *,
      start_station: str ) -> list[ TransportationRouteLegSegment ]:
   if not legs:
      return []

   outgoing_by_from: dict[ str, TransportationRouteLegSegment ] = {}

   for leg in legs:
      if leg.from_station in outgoing_by_from:
         raise ValueError(
            f'Duplicate outgoing leg from station { repr( leg.from_station ) }' )

      outgoing_by_from[ leg.from_station ] = leg

   ordered: list[ TransportationRouteLegSegment ] = []
   current_station = start_station

   for _ in range( len( outgoing_by_from ) ):
      next_leg = outgoing_by_from.get( current_station )

      if next_leg is None:
         raise ValueError(
            f'No outgoing leg from station { repr( current_station ) }' )

      ordered.append( next_leg )
      current_station = next_leg.to_station

   if current_station != start_station:
      raise ValueError(
         f'Route legs from { repr( start_station ) } do not form a closed loop' )

   return ordered


def fetch_transportation_day_loop(
      conn: Connection,
      *,
      transportation: str,
      target_date: date ) -> TransportationDayLoop | None:
   main_station = fetch_main_transportation_station( conn, transportation )

   if main_station is None:
      return None

   route = resolve_transportation_route_for_date(
      conn,
      transportation=transportation,
      target_date=target_date )
   leg_rows = fetch_transportation_route_legs(
      conn,
      transportation=transportation,
      route=route )

   if not leg_rows:
      return None

   return TransportationDayLoop(
      transportation=transportation,
      route=route,
      main_station=main_station,
      legs=order_route_legs_from_station(
         leg_rows,
         start_station=main_station ) )
