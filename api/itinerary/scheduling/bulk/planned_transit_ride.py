from __future__ import annotations

from dataclasses import dataclass

from ...transportation.transportation_route_leg_segment import TransportationRouteLegSegment


@dataclass( frozen=True )
class PlannedTransitRide:
   from_station: str
   to_station: str
   legs: list[ TransportationRouteLegSegment ]
   remaining_walk_px: float
