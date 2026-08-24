from __future__ import annotations

from ...shared.duration_values import duration_minutes_to_seconds
from .transportation_day_loop import TransportationDayLoop
from .transportation_route_leg_segment import TransportationRouteLegSegment


def legs_along_day_loop(
      day_loop: TransportationDayLoop,
      from_station: str,
      to_station: str ) -> list[ TransportationRouteLegSegment ]:
   if from_station == to_station:
      return []

   legs_by_from = {
      leg.from_station: leg
      for leg in day_loop.legs
   }
   ordered: list[ TransportationRouteLegSegment ] = []
   current = from_station

   for _ in range( len( day_loop.legs ) ):
      leg = legs_by_from.get( current )

      if leg is None:
         return []

      ordered.append( leg )
      current = leg.to_station

      if current == to_station:
         return ordered

   return []


def ride_duration_seconds(
      day_loop: TransportationDayLoop,
      from_station: str,
      to_station: str ) -> int:
   return duration_minutes_to_seconds(
      sum(
         leg.duration_minutes
         for leg in legs_along_day_loop(
            day_loop,
            from_station,
            to_station ) ) )
