from __future__ import annotations

from ..scheduling.current_route_schedule import TransportationCurrentRouteSchedule
from ...types import Connection


class TransportationRouteScheduleProvider():
   @classmethod
   def save_current_transportation_route_schedule(
         cls,
         conn: Connection,
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
