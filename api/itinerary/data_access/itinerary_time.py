from __future__ import annotations

from ...types import Connection, ScheduleTimeKey


def set_itinerary_arrival_time(
      conn: Connection,
      arrival_time: ScheduleTimeKey ) -> bool:
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


def set_itinerary_departure_time(
      conn: Connection,
      departure_time: ScheduleTimeKey ) -> bool:
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
