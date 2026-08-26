from __future__ import annotations

from datetime import date

from ...types import Connection


class TransportationActiveRouteProvider():
   @classmethod
   def fetch_transportation_route_ids(
         cls,
         conn: Connection,
         transportation: str ) -> list[ str ]:
      cur = conn.cursor()
      try:
         data = cur.execute(
            """   SELECT
                     r.ROUTE
                  FROM TransportationRoute r
                  WHERE r.TRANSPORTATION = ?;
            """,
            ( transportation, ) )
         return [ row[ 0 ] for row in data.fetchall() ]
      finally:
         cur.close()


   @classmethod
   def fetch_transportation_route_station_names(
         cls,
         conn: Connection,
         transportation: str,
         route: str ) -> list[ str ]:
      cur = conn.cursor()
      try:
         data = cur.execute(
            """   SELECT
                     rs.STATION
                  FROM TransportationRouteStation rs
                  WHERE rs.TRANSPORTATION = ?
                  AND rs.ROUTE = ?;
            """,
            ( transportation, route ) )
         return [ row[ 0 ] for row in data.fetchall() ]
      finally:
         cur.close()


   @classmethod
   def fetch_active_transportation_route(
         cls,
         conn: Connection,
         transportation: str,
         target_date: date ) -> str | None:
      cur = conn.cursor()
      try:
         data = cur.execute(
            """   SELECT
                     ROUTE
                  FROM TransportationRouteSchedule
                  WHERE TRANSPORTATION = ?
                    AND SCHEDULE_START_DATE <= ?
                  AND (
                     SCHEDULE_END_DATE IS NULL
                     OR SCHEDULE_END_DATE >= ?
                  )
                  ORDER BY SCHEDULE_START_DATE DESC
                  LIMIT 1;
            """,
            (
               transportation,
               target_date.isoformat(),
               target_date.isoformat(),
            ) )
         route_data = data.fetchone()
         if route_data is None:
            return None
         return route_data[ 'ROUTE' ]
      finally:
         cur.close()


   @classmethod
   def fetch_transportation_day_route(
         cls,
         conn: Connection,
         transportation: str,
         month: int,
         day: int ) -> str | None:
      cur = conn.cursor()
      try:
         data = cur.execute(
            """   SELECT
                     z.ROUTE
                  FROM TransportationDayRoute z
                  WHERE z.TRANSPORTATION = ?
                  AND z.MONTH = ?
                  AND z.DAY = ?;
            """, ( transportation, month, day ) )
         route_data = data.fetchone()
         if route_data is None:
            return None
         return route_data[ 'ROUTE' ]
      finally:
         cur.close()
