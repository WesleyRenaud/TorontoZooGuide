from __future__ import annotations

from .itinerary_walk_route_leg_mapper import map_itinerary_walk_route_leg_records
from .itinerary_walk_route_leg_mapper import map_itinerary_walk_route_legs
from .itinerary_walk_route_leg_record import ItineraryWalkRouteLegRecord
from .itinerary_walk_route_point_mapper import map_itinerary_walk_route_point_records
from .itinerary_walk_route_point_mapper import map_itinerary_walk_route_points
from .itinerary_walk_route_point_record import ItineraryWalkRoutePointRecord
from .itinerary_walk_route_stop_mapper import map_itinerary_walk_route_stop_records
from .itinerary_walk_route_stop_mapper import map_itinerary_walk_route_stops
from .itinerary_walk_route_stop_record import ItineraryWalkRouteStopRecord
from ..routing.itinerary_walk_route import empty_itinerary_walk_route
from ..routing.itinerary_walk_route import ItineraryWalkRoute
from ...types import Connection


def fetch_itinerary_walk_route_leg_rows(
      conn: Connection ) -> list[ ItineraryWalkRouteLegRecord ]:
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT
               LEG_SEQUENCE,
               FROM_ITEM_KEY,
               TO_ITEM_KEY,
               FROM_SCHEDULE_ITEM_KIND,
               TO_SCHEDULE_ITEM_KIND,
               FROM_POINT_SEQUENCE,
               TO_POINT_SEQUENCE
            FROM ItineraryWalkRouteLeg
            ORDER BY LEG_SEQUENCE;
      """
   ).fetchall()

   cur.close()

   return map_itinerary_walk_route_leg_records( rows )


def fetch_itinerary_walk_route_stop_rows(
      conn: Connection ) -> list[ ItineraryWalkRouteStopRecord ]:
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT
               STOP_SEQUENCE,
               SCHEDULE_ITEM_KIND,
               ITEM_KEY,
               WALK_NODE_ID,
               START_TIME,
               END_TIME
            FROM ItineraryWalkRouteStop
            ORDER BY STOP_SEQUENCE;
      """
   ).fetchall()

   cur.close()

   return map_itinerary_walk_route_stop_records( rows )


def fetch_itinerary_walk_route_point_rows(
      conn: Connection ) -> list[ ItineraryWalkRoutePointRecord ]:
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT
               POINT_SEQUENCE,
               WALK_NODE_ID,
               X,
               Y,
               X_PX,
               Y_PX
            FROM ItineraryWalkRoutePoint
            ORDER BY POINT_SEQUENCE;
      """
   ).fetchall()

   cur.close()

   return map_itinerary_walk_route_point_records( rows )


def fetch_itinerary_walk_route( conn: Connection ) -> ItineraryWalkRoute:
   leg_rows = fetch_itinerary_walk_route_leg_rows( conn )

   if not leg_rows:
      return empty_itinerary_walk_route()

   stop_rows = fetch_itinerary_walk_route_stop_rows( conn )
   point_rows = fetch_itinerary_walk_route_point_rows( conn )
   points = map_itinerary_walk_route_points( point_rows )

   return ItineraryWalkRoute(
      stops=map_itinerary_walk_route_stops( stop_rows ),
      legs=map_itinerary_walk_route_legs( leg_rows, points ),
      points=points )
