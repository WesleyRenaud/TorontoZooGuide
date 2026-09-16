from __future__ import annotations

from ...shared.enums.position import Position
from ...types import Types


class RestroomAlertNameProvider():
   @classmethod
   def fetch_restroom_alert_names(
         cls,
         conn: Types.Connection,
         today: Types.DateKey ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     RESTROOM
                  FROM RestroomAlert
                  WHERE ALERT_END_DATE IS NULL
                     OR ALERT_END_DATE >= ?
                  ORDER BY RESTROOM;
            """,
            ( today, ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()
