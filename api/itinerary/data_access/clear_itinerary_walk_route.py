from __future__ import annotations

from ...types import Cursor


def clear_itinerary_walk_route_stops( cur: Cursor ) -> None:
   cur.execute( 'DELETE FROM ItineraryWalkRouteStop;' )


def clear_itinerary_walk_route_points( cur: Cursor ) -> None:
   cur.execute( 'DELETE FROM ItineraryWalkRoutePoint;' )


def clear_itinerary_walk_route_legs( cur: Cursor ) -> None:
   cur.execute( 'DELETE FROM ItineraryWalkRouteLeg;' )


def clear_itinerary_walk_route( cur: Cursor ) -> None:
   clear_itinerary_walk_route_legs( cur )
   clear_itinerary_walk_route_points( cur )
   clear_itinerary_walk_route_stops( cur )
