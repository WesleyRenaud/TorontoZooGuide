from __future__ import annotations

from ...shared.enums.position import Position
from ...types import Types


class AnimalEnclosureExhibitNameProvider():
   @classmethod
   def fetch_exhibit_names_for_species(
         cls,
         conn: Types.Connection,
         species: str ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     EXHIBIT
                  FROM Enclosure
                  WHERE SPECIES = ?
                  ORDER BY EXHIBIT;
            """,
            ( species, ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()
