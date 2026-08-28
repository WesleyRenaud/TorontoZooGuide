from __future__ import annotations

from dataclasses import dataclass

from ...shared.duration_values import DurationValues
from .transportation_route_leg_segment import TransportationRouteLegSegment


@dataclass( frozen=True )
class TransportationDayLoop:
   transportation: str
   route: str
   main_station: str
   legs: list[ TransportationRouteLegSegment ]


   def duration_minutes( self ) -> int:
      return sum( leg.duration_minutes for leg in self.legs )


   def duration_seconds( self ) -> int:
      return DurationValues.minutes_to_seconds( self.duration_minutes() )
