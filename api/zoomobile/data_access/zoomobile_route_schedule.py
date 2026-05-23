from __future__ import annotations

from ...types import Connection
from ..logic.zoomobile_current_route_schedule import ZoomobileCurrentRouteSchedule


def save_current_zoomobile_route_schedule(
      conn: Connection,
      schedule: ZoomobileCurrentRouteSchedule ) -> bool:
   cur = conn.cursor()

   try:
      cur.execute( 'DELETE FROM ZoomobileRouteSchedule;' )

      cur.execute(
         """   INSERT INTO ZoomobileRouteSchedule (
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  ROUTE
               )
               VALUES ( ?, ?, ? );
         """,
         (
            schedule.start_date,
            schedule.end_date,
            schedule.route,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
