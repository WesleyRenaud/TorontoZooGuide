from __future__ import annotations

from ...shared.enums.position import Position
from ...types import Types


class AnimalOffDisplaySpeciesNameProvider():
   @classmethod
   def fetch_off_display_species_names(
         cls,
         conn: Types.Connection,
         today: Types.DateKey,
         for_season_only: bool ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     SPECIES
                  FROM AnimalStatus
                  WHERE IS_OFF_DISPLAY = 1
                     AND (
                        OFF_DISPLAY_END IS NULL
                        OR OFF_DISPLAY_END >= ?
                     )
                     AND (
                        ? = 0
                        OR OFF_DISPLAY_FOR_SEASON = 1
                     )
                  ORDER BY SPECIES;
            """,
            ( today, for_season_only ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()


   @classmethod
   def fetch_off_display_species_names_in_exhibit(
         cls,
         conn: Types.Connection,
         today: Types.DateKey,
         exhibit: str,
         for_season_only: bool ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     SPECIES
                  FROM AnimalStatus
                  WHERE IS_OFF_DISPLAY = 1
                     AND (
                        OFF_DISPLAY_END IS NULL
                        OR OFF_DISPLAY_END >= ?
                     )
                     AND (
                        ? = 0
                        OR OFF_DISPLAY_FOR_SEASON = 1
                     )
                     AND EXHIBIT = ?
                  ORDER BY SPECIES;
            """,
            ( today, for_season_only, exhibit ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()
