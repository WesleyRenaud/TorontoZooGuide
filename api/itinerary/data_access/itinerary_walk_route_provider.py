from __future__ import annotations

from .itinerary_walk_route_leg_mapper import ItineraryWalkRouteLegMapper
from .itinerary_walk_route_leg_record import ItineraryWalkRouteLegRecord
from .itinerary_walk_route_point_mapper import ItineraryWalkRoutePointMapper
from .itinerary_walk_route_point_record import ItineraryWalkRoutePointRecord
from .itinerary_walk_route_stop_mapper import ItineraryWalkRouteStopMapper
from .itinerary_walk_route_stop_record import ItineraryWalkRouteStopRecord
from ..routing.itinerary_walk_route import empty_itinerary_walk_route
from ..routing.itinerary_walk_route import ItineraryWalkRoute
from ..routing.walk_route_polyline import inclusive_point_slices_for_walk_route_legs
from ...types import Connection, Cursor


class ItineraryWalkRouteProvider():
   @classmethod
   def fetch_itinerary_walk_route_leg_rows(
         cls,
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
                  TO_POINT_SEQUENCE,
                  TRAVEL_TIME_MINUTES
               FROM ItineraryWalkRouteLeg
               ORDER BY LEG_SEQUENCE;
         """
      ).fetchall()

      cur.close()

      return ItineraryWalkRouteLegMapper.map_records( rows )


   @classmethod
   def fetch_itinerary_walk_route_stop_rows(
         cls,
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

      return ItineraryWalkRouteStopMapper.map_records( rows )


   @classmethod
   def fetch_itinerary_walk_route_point_rows(
         cls,
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

      return ItineraryWalkRoutePointMapper.map_records( rows )


   @classmethod
   def fetch_itinerary_walk_route( cls, conn: Connection ) -> ItineraryWalkRoute:
      leg_rows = cls.fetch_itinerary_walk_route_leg_rows( conn )

      if not leg_rows:
         return empty_itinerary_walk_route()

      stop_rows = cls.fetch_itinerary_walk_route_stop_rows( conn )
      point_rows = cls.fetch_itinerary_walk_route_point_rows( conn )
      points = ItineraryWalkRoutePointMapper.map_to_walk_route_points( point_rows )

      return ItineraryWalkRoute(
         stops=ItineraryWalkRouteStopMapper.map_to_walk_route_stops( stop_rows ),
         legs=ItineraryWalkRouteLegMapper.map_to_walk_route_legs( leg_rows, points ),
         points=points )


   @classmethod
   def clear_itinerary_walk_route_stops( cls, cur: Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryWalkRouteStop;' )


   @classmethod
   def clear_itinerary_walk_route_points( cls, cur: Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryWalkRoutePoint;' )


   @classmethod
   def clear_itinerary_walk_route_legs( cls, cur: Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryWalkRouteLeg;' )


   @classmethod
   def clear_itinerary_walk_route( cls, cur: Cursor ) -> None:
      cls.clear_itinerary_walk_route_legs( cur )
      cls.clear_itinerary_walk_route_points( cur )
      cls.clear_itinerary_walk_route_stops( cur )


   @classmethod
   def save_itinerary_walk_route(
         cls,
         conn: Connection,
         walk_route: ItineraryWalkRoute ) -> bool:
      cur = conn.cursor()

      try:
         cls.clear_itinerary_walk_route( cur )

         if walk_route.legs:
            cls.insert_itinerary_walk_route_stops( cur, walk_route )
            cls.insert_itinerary_walk_route_points( cur, walk_route )
            cls.insert_itinerary_walk_route_legs( cur, walk_route )

         conn.commit()

      finally:
         cur.close()

      return True


   @classmethod
   def insert_itinerary_walk_route_stops(
         cls,
         cur: Cursor,
         walk_route: ItineraryWalkRoute ) -> None:
      for stop_sequence, stop in enumerate( walk_route.stops ):
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


   @classmethod
   def insert_itinerary_walk_route_points(
         cls,
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


   @classmethod
   def insert_itinerary_walk_route_legs(
         cls,
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
                     TO_POINT_SEQUENCE,
                     TRAVEL_TIME_MINUTES
                  )
                  VALUES ( ?, ?, ?, ?, ?, ?, ?, ? );
            """,
            (
               leg_sequence,
               leg.from_item_key,
               leg.to_item_key,
               leg.from_schedule_item_kind.value,
               leg.to_schedule_item_kind.value,
               from_point_sequence,
               to_point_sequence,
               leg.travel_time_minutes,
            ) )
