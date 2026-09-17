from __future__ import annotations

from ...shared.enums.position import Position
from ...types import Types


class AnimalOffDisplayExhibitNameProvider():
   @classmethod
   def fetch_off_display_exhibit_names(
         cls,
         conn: Types.Connection,
         today: Types.DateKey ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     EXHIBIT
                  FROM AnimalStatus
                  WHERE IS_OFF_DISPLAY = 1
                     AND (
                        OFF_DISPLAY_END IS NULL
                        OR OFF_DISPLAY_END >= ?
                     )
                  ORDER BY EXHIBIT;
            """,
            ( today, ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()


   @classmethod
   def fetch_off_display_exhibit_names_for_species(
         cls,
         conn: Types.Connection,
         today: Types.DateKey,
         species: str ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     EXHIBIT
                  FROM AnimalStatus
                  WHERE IS_OFF_DISPLAY = 1
                     AND (
                        OFF_DISPLAY_END IS NULL
                        OR OFF_DISPLAY_END >= ?
                     )
                     AND SPECIES = ?
                  ORDER BY EXHIBIT;
            """,
            ( today, species ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()
