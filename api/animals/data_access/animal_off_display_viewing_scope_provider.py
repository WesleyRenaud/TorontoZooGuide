from __future__ import annotations

from ..domain.animal_viewing_scope import AnimalViewingScope
from ...types import Types


class AnimalOffDisplayViewingScopeProvider():
   @classmethod
   def fetch_off_display_viewing_scopes(
         cls,
         conn: Types.Connection,
         today: Types.DateKey,
         species: str,
         exhibit: str ) -> list[ AnimalViewingScope ]:
      cur = conn.cursor()

      try:
         rows = cur.execute(
            """   SELECT VIEWING_SCOPE
                  FROM AnimalStatus
                  WHERE IS_OFF_DISPLAY = 1
                     AND (
                        OFF_DISPLAY_END IS NULL
                        OR OFF_DISPLAY_END >= ?
                     )
                     AND SPECIES = ?
                     AND EXHIBIT = ?
                  ORDER BY VIEWING_SCOPE;
            """,
            (
               today,
               species,
               exhibit,
            ) ).fetchall()

         return [
            AnimalViewingScope.from_enclosure_name( row[ 'VIEWING_SCOPE' ] )
            for row in rows
         ]

      finally:
         cur.close()
