from __future__ import annotations

from ..scheduling.transportation_current_route_schedule import TransportationCurrentRouteSchedule
from .transportation_route_schedule_mapper import TransportationRouteScheduleMapper
from ...types import Types


class TransportationRouteScheduleProvider():
   @classmethod
   def fetch_transportation_route_schedules(
         cls,
         conn: Types.Connection,
         transportation: str ) -> list[ TransportationCurrentRouteSchedule ]:
      cur = conn.cursor()
      try:
         rows = cur.execute(
            """   SELECT
                     s.ROUTE,
                     s.SCHEDULE_START_DATE,
                     s.SCHEDULE_END_DATE
                  FROM TransportationRouteSchedule s
                  WHERE s.TRANSPORTATION = ?;
            """,
            ( transportation, ),
         ).fetchall()
         return TransportationRouteScheduleMapper.map_records( rows )
      finally:
         cur.close()


   @classmethod
   def save_current_transportation_route_schedule(
         cls,
         conn: Types.Connection,
         transportation: str,
         schedule: TransportationCurrentRouteSchedule ) -> bool:
      cur = conn.cursor()
      try:
         cur.execute(
            """   INSERT OR REPLACE INTO TransportationRouteSchedule (
                     TRANSPORTATION,
                     SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE,
                     ROUTE
                  )
                  VALUES ( ?, ?, ?, ? );
            """,
            (
               transportation,
               schedule.start_date,
               schedule.end_date,
               schedule.route,
            ) )
         conn.commit()
         return cur.rowcount > 0
      finally:
         cur.close()
