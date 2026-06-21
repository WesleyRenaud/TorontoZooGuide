from __future__ import annotations

from .clear_itinerary_walk_route import clear_itinerary_walk_route
from ..routing.itinerary_walk_route import ItineraryWalkRoute
from ..routing.walk_route_polyline import inclusive_point_slices_for_walk_route_legs
from ...types import Connection, Cursor


def save_itinerary_walk_route(
      conn: Connection,
      walk_route: ItineraryWalkRoute ) -> bool:
   cur = conn.cursor()

   try:
      clear_itinerary_walk_route( cur )

      if walk_route.legs:
         insert_itinerary_walk_route_stops( cur, walk_route )
         insert_itinerary_walk_route_points( cur, walk_route )
         insert_itinerary_walk_route_legs( cur, walk_route )

      conn.commit()

   finally:
      cur.close()

   return True


def insert_itinerary_walk_route_stops(
      cur: Cursor,
      walk_route: ItineraryWalkRoute ) -> None:
   for stop_sequence, stop in enumerate( walk_route.stops ):
      assert stop.walk_node_id is not None

      cur.execute(
         """   INSERT INTO ItineraryWalkRouteStop (
                  STOP_SEQUENCE,
                  SCHEDULE_ITEM_KIND,
                  ITEM_KEY,
                  WALK_NODE_ID,
                  START_TIME,
                  END_TIME
               )
               VALUES ( ?, ?, ?, ?, ?, ? );
         """,
         (
            stop_sequence,
            stop.schedule_item_kind.value,
            stop.item_key,
            stop.walk_node_id,
            stop.start_time,
            stop.end_time,
         ) )


def insert_itinerary_walk_route_points(
      cur: Cursor,
      walk_route: ItineraryWalkRoute ) -> None:
   for point_sequence, point in enumerate( walk_route.points ):
      cur.execute(
         """   INSERT INTO ItineraryWalkRoutePoint (
                  POINT_SEQUENCE,
                  WALK_NODE_ID,
                  X,
                  Y,
                  X_PX,
                  Y_PX
               )
               VALUES ( ?, ?, ?, ?, ?, ? );
         """,
         (
            point_sequence,
            point.node_id,
            point.x,
            point.y,
            point.x_px,
            point.y_px,
         ) )


def insert_itinerary_walk_route_legs(
      cur: Cursor,
      walk_route: ItineraryWalkRoute ) -> None:
   leg_point_slices = inclusive_point_slices_for_walk_route_legs(
      walk_route.legs )

   for leg_sequence, ( leg, point_slice ) in enumerate(
         zip( walk_route.legs, leg_point_slices ) ):
      from_point_sequence, to_point_sequence = point_slice

      cur.execute(
         """   INSERT INTO ItineraryWalkRouteLeg (
                  LEG_SEQUENCE,
                  FROM_ITEM_KEY,
                  TO_ITEM_KEY,
                  FROM_SCHEDULE_ITEM_KIND,
                  TO_SCHEDULE_ITEM_KIND,
                  FROM_POINT_SEQUENCE,
                  TO_POINT_SEQUENCE
               )
               VALUES ( ?, ?, ?, ?, ?, ?, ? );
         """,
         (
            leg_sequence,
            leg.from_item_key,
            leg.to_item_key,
            leg.from_schedule_item_kind.value,
            leg.to_schedule_item_kind.value,
            from_point_sequence,
            to_point_sequence,
         ) )

