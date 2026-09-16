from __future__ import annotations

from ...shared.enums.position import Position
from ...types import Types


class ClosedRestroomNameProvider():
   @classmethod
   def fetch_closed_restroom_names(
         cls,
         conn: Types.Connection,
         today: Types.DateKey ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     RESTROOM
                  FROM RestroomStatus
                  WHERE IS_CLOSED = 1
                     AND (
                        CLOSED_END IS NULL
                        OR CLOSED_END >= ?
                     )
                  ORDER BY RESTROOM;
            """,
            ( today, ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()
