from __future__ import annotations

from dataclasses import dataclass

from .itinerary_walk_route_stop import ItineraryWalkRouteStop
from .walk_route_leg import WalkRouteLeg
from .walk_route_point import WalkRoutePoint


@dataclass( frozen=True )
class ItineraryWalkRoute:
   stops: list[ ItineraryWalkRouteStop ]
   legs: list[ WalkRouteLeg ]
   points: list[ WalkRoutePoint ]

   def to_dict( self ) -> dict[ str, object ]:
      return {
         'stops': [ stop.to_dict() for stop in self.stops ],
         'legs': [ leg.to_dict() for leg in self.legs ],
         'points': [ point.to_dict() for point in self.points ],
      }


def empty_itinerary_walk_route() -> ItineraryWalkRoute:
   return ItineraryWalkRoute(
      stops=[],
      legs=[],
      points=[] )
