from __future__ import annotations

from ...types import Types


class ItineraryTimeProvider():
   @classmethod
   def set_itinerary_arrival_time(
         cls,
         conn: Types.Connection,
         arrival_time: Types.ScheduleTimeKey ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   UPDATE ItineraryDate
                  SET ARRIVAL_TIME = ?;
            """,
            ( arrival_time, ) )
         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def set_itinerary_departure_time(
         cls,
         conn: Types.Connection,
         departure_time: Types.ScheduleTimeKey ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   UPDATE ItineraryDate
                  SET DEPARTURE_TIME = ?;
            """,
            ( departure_time, ) )
         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()
