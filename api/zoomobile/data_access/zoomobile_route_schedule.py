from __future__ import annotations

from ..scheduling.zoomobile_current_route_schedule import ZoomobileCurrentRouteSchedule
from ...shared.enums.transportation_name import TransportationName
from ...types import Connection


def save_current_zoomobile_route_schedule(
      conn: Connection,
      schedule: ZoomobileCurrentRouteSchedule ) -> bool:
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
            TransportationName.ZOOMOBILE,
            schedule.start_date,
            schedule.end_date,
            schedule.route,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
