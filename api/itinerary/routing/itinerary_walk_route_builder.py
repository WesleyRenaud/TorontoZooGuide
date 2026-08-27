from __future__ import annotations

from .itinerary_walk_route import ItineraryWalkRoute


class ItineraryWalkRouteBuilder():
   @classmethod
   def empty( cls ) -> ItineraryWalkRoute:
      return ItineraryWalkRoute(
         stops=[],
         legs=[],
         points=[] )
