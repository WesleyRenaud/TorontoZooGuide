from __future__ import annotations

from ...shared.enums.position import Position
from ...types import Types


class AnimalVisibilityScheduleExhibitNameProvider():
   @classmethod
   def fetch_visibility_schedule_exhibit_names(
         cls,
         conn: Types.Connection,
         today: Types.DateKey ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     EXHIBIT
                  FROM AnimalVisibilitySchedule
                  WHERE SCHEDULE_END_DATE IS NULL
                     OR SCHEDULE_END_DATE >= ?
                  ORDER BY EXHIBIT;
            """,
            ( today, ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()
