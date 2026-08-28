from __future__ import annotations

from .itinerary_transportation_route_marker_provider import ItineraryTransportationRouteMarkerProvider
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...shared.calendar_dates import DateValues
from ...types import Types


class ItineraryTransportationProvider():
   @classmethod
   def insert_itinerary_transportation(
         cls,
         cur: Types.Cursor,
         transportation: str,
         old_likelihood: int | None,
         new_likelihood: int | None,
         added_as_attraction: bool,
         start_time: Types.ScheduleTimeKey = None,
         end_time: Types.ScheduleTimeKey = None,
         route: str | None = None,
         bulk_transit_evaluated: bool = False,
   ) -> bool:
      cur.execute(
         """   INSERT OR IGNORE INTO ItineraryTransportation (
                  TRANSPORTATION,
                  OLD_LIKELIHOOD,
                  NEW_LIKELIHOOD,
                  ADDED_AS_ATTRACTION,
                  START_TIME,
                  END_TIME,
                  ROUTE,
                  BULK_TRANSIT_EVALUATED
               )
               VALUES ( ?, ?, ?, ?, ?, ?, ?, ? );
         """,
         (
            transportation,
            old_likelihood,
            new_likelihood,
            added_as_attraction,
            DateValues.normalize_itinerary_schedule_time( start_time ),
            DateValues.normalize_itinerary_schedule_time( end_time ),
            route,
            bulk_transit_evaluated,
         ),
      )

      return cur.rowcount > 0


   @classmethod
   def insert_itinerary_transportation_legs(
         cls,
         cur: Types.Cursor,
         transportation: str,
         added_as_attraction: bool,
         legs: list[ ItineraryTransportationLeg ] ) -> None:
      for leg in legs:
         cur.execute(
            """   INSERT INTO ItineraryTransportationLeg (
                     TRANSPORTATION,
                     ADDED_AS_ATTRACTION,
                     FROM_STATION,
                     TO_STATION,
                     START_TIME,
                     END_TIME
                  )
                  VALUES ( ?, ?, ?, ?, ?, ? );
            """,
            (
               transportation,
               added_as_attraction,
               leg.from_station,
               leg.to_station,
               DateValues.normalize_itinerary_schedule_time( leg.start_time ),
               DateValues.normalize_itinerary_schedule_time( leg.end_time ),
            ),
         )


   @classmethod
   def delete_itinerary_transportation_legs(
         cls,
         cur: Types.Cursor,
         transportation: str,
         added_as_attraction: bool ) -> None:
      cur.execute(
         """   DELETE FROM ItineraryTransportationLeg
               WHERE TRANSPORTATION = ?
                 AND ADDED_AS_ATTRACTION = ?;
         """,
         ( transportation, added_as_attraction ),
      )


   @classmethod
   def clear_itinerary_transportation_legs( cls, cur: Types.Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryTransportationLeg;' )


   @classmethod
   def delete_itinerary_transportation_row(
         cls,
         cur: Types.Cursor,
         transportation: str,
         added_as_attraction: bool ) -> None:
      cur.execute(
         """   DELETE FROM ItineraryTransportation
               WHERE TRANSPORTATION = ?
                 AND ADDED_AS_ATTRACTION = ?;
         """,
         ( transportation, added_as_attraction ),
      )


   @classmethod
   def clear_itinerary_transportation_rows( cls, cur: Types.Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryTransportation;' )


   @classmethod
   def set_itinerary_transportation_bulk_transit_evaluated(
         cls,
         cur: Types.Cursor,
         transportation: str,
         added_as_attraction: bool,
         *,
         bulk_transit_evaluated: bool,
   ) -> None:
      cur.execute(
         """   UPDATE ItineraryTransportation
               SET BULK_TRANSIT_EVALUATED = ?
               WHERE TRANSPORTATION = ?
                 AND ADDED_AS_ATTRACTION = ?;
         """,
         ( bulk_transit_evaluated, transportation, added_as_attraction ),
      )


   @classmethod
   def clear_itinerary_transportation_schedule_times(
         cls,
         cur: Types.Cursor,
         transportation: str,
         added_as_attraction: bool ) -> None:
      cur.execute(
         """   UPDATE ItineraryTransportation
               SET START_TIME = NULL,
                   END_TIME = NULL,
                   ROUTE = NULL,
                   BULK_TRANSIT_EVALUATED = 0
               WHERE TRANSPORTATION = ?
                 AND ADDED_AS_ATTRACTION = ?;
         """,
         ( transportation, added_as_attraction ),
      )


   @classmethod
   def clear_all_itinerary_transportation_schedule_times( cls, cur: Types.Cursor ) -> None:
      cur.execute(
         """   UPDATE ItineraryTransportation
               SET START_TIME = NULL,
                   END_TIME = NULL,
                   ROUTE = NULL,
                   BULK_TRANSIT_EVALUATED = 0;
         """ )


   @classmethod
   def delete_itinerary_transportation(
         cls,
         cur: Types.Cursor,
         transportation: str,
         added_as_attraction: bool ) -> None:
      ItineraryTransportationRouteMarkerProvider.delete_itinerary_transportation_route_markers(
         cur,
         transportation=transportation,
         added_as_attraction=added_as_attraction )
      cls.delete_itinerary_transportation_legs(
         cur,
         transportation=transportation,
         added_as_attraction=added_as_attraction )
      cls.delete_itinerary_transportation_row(
         cur,
         transportation=transportation,
         added_as_attraction=added_as_attraction )


   @classmethod
   def clear_itinerary_transportations( cls, cur: Types.Cursor ) -> None:
      ItineraryTransportationRouteMarkerProvider.clear_itinerary_transportation_route_markers( cur )
      cls.clear_itinerary_transportation_legs( cur )
      cls.clear_itinerary_transportation_rows( cur )
