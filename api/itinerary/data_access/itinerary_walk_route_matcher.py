from __future__ import annotations

from ..routing.itinerary_walk_route import ItineraryWalkRoute


class ItineraryWalkRouteMatcher():
   @classmethod
   def matches(
         cls,
         left: ItineraryWalkRoute,
         right: ItineraryWalkRoute ) -> bool:
      if len( left.stops ) != len( right.stops ):
         return False

      if len( left.legs ) != len( right.legs ):
         return False

      if len( left.points ) != len( right.points ):
         return False

      for left_stop, right_stop in zip( left.stops, right.stops ):
         if left_stop != right_stop:
            return False

      for left_leg, right_leg in zip( left.legs, right.legs ):
         if left_leg != right_leg:
            return False

      for left_point, right_point in zip( left.points, right.points ):
         if left_point != right_point:
            return False

      return True
