from __future__ import annotations

from ...shared.enums.position import Position
from ...types import Types


class AnimalViewingAlertSpeciesNameProvider():
   @classmethod
   def fetch_viewing_alert_species_names(
         cls,
         conn: Types.Connection,
         today: Types.DateKey ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     SPECIES
                  FROM AnimalViewingAlert
                  WHERE ALERT_END_DATE IS NULL
                     OR ALERT_END_DATE >= ?
                  ORDER BY SPECIES;
            """,
            ( today, ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()


   @classmethod
   def fetch_viewing_alert_species_names_in_exhibit(
         cls,
         conn: Types.Connection,
         today: Types.DateKey,
         exhibit: str ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     SPECIES
                  FROM AnimalViewingAlert
                  WHERE (
                        ALERT_END_DATE IS NULL
                        OR ALERT_END_DATE >= ?
                     )
                     AND EXHIBIT = ?
                  ORDER BY SPECIES;
            """,
            ( today, exhibit ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()
