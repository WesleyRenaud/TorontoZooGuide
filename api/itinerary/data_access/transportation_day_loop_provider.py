from __future__ import annotations

from datetime import date

from ..transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from .transportation_route_leg_segment_mapper import TransportationRouteLegSegmentMapper
from ...types import Types


class TransportationDayLoopProvider():
   @classmethod
   def fetch_transportation_active_route(
         cls,
         conn: Types.Connection,
         *,
         transportation: str,
         target_date: date ) -> str | None:
      cur = conn.cursor()

      try:
         row = cur.execute(
            """   SELECT ROUTE
                  FROM TransportationRouteSchedule
                  WHERE TRANSPORTATION = ?
                    AND SCHEDULE_START_DATE <= ?
                    AND ( SCHEDULE_END_DATE IS NULL
                          OR SCHEDULE_END_DATE >= ? )
                  ORDER BY SCHEDULE_START_DATE DESC
                  LIMIT 1;
            """,
            (
               transportation,
               target_date.isoformat(),
               target_date.isoformat(),
            ),
         ).fetchone()

         if row is None:
            return None

         return row[ 'ROUTE' ]

      finally:
         cur.close()


   @classmethod
   def fetch_transportation_day_route(
         cls,
         conn: Types.Connection,
         *,
         transportation: str,
         month: int,
         day: int ) -> str | None:
      cur = conn.cursor()

      try:
         row = cur.execute(
            """   SELECT ROUTE
                  FROM TransportationDayRoute
                  WHERE TRANSPORTATION = ?
                    AND MONTH = ?
                    AND DAY = ?;
            """,
            ( transportation, month, day ),
         ).fetchone()

         if row is None:
            return None

         return row[ 'ROUTE' ]

      finally:
         cur.close()


   @classmethod
   def fetch_main_transportation_station(
         cls,
         conn: Types.Connection,
         transportation: str ) -> str | None:
      cur = conn.cursor()

      try:
         row = cur.execute(
            """   SELECT NAME
                  FROM TransportationStation
                  WHERE TRANSPORTATION = ?
                    AND IS_MAIN_STATION = 1;
            """,
            ( transportation, ),
         ).fetchone()

         if row is None:
            return None

         return row[ 'NAME' ]

      finally:
         cur.close()


   @classmethod
   def fetch_transportation_route_legs(
         cls,
         conn: Types.Connection,
         *,
         transportation: str,
         route: str ) -> list[ TransportationRouteLegSegment ]:
      cur = conn.cursor()

      try:
         rows = cur.execute(
            """   SELECT
                     rl.FROM_STATION,
                     rl.TO_STATION,
                     l.DURATION_MINUTES
                  FROM TransportationRouteLeg rl
                  JOIN TransportationLeg l
                    ON l.TRANSPORTATION = rl.TRANSPORTATION
                   AND l.FROM_STATION = rl.FROM_STATION
                   AND l.TO_STATION = rl.TO_STATION
                  WHERE rl.TRANSPORTATION = ?
                    AND rl.ROUTE = ?;
            """,
            ( transportation, route ),
         ).fetchall()

         return TransportationRouteLegSegmentMapper.map_records( rows )

      finally:
         cur.close()
