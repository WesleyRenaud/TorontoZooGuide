from __future__ import annotations

from ...types import Types


class AnimalSpeciesNameProvider():
   @classmethod
   def fetch_animal_species_names( cls, conn: Types.Connection ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     a.SPECIES
                  FROM Animal a;
            """ )

         return [ row[ 0 ] for row in data.fetchall() ]

      finally:
         cur.close()
