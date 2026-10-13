from __future__ import annotations

from ...shared.enums.position import Position
from ...types import Types


class ClosedExhibitNameProvider():
   @classmethod
   def fetch_closed_exhibit_names(
         cls,
         conn: Types.Connection,
         today: Types.DateKey,
         for_season_only: bool ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     EXHIBIT
                  FROM ExhibitStatus
                  WHERE IS_CLOSED = 1
                     AND (
                        CLOSED_END IS NULL
                        OR CLOSED_END >= ?
                     )
                     AND (
                        ? = 0
                        OR CLOSED_FOR_SEASON = 1
                     )
                  ORDER BY EXHIBIT;
            """,
            ( today, for_season_only ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()
