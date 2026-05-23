from __future__ import annotations

from ...types import Connection


def fetch_animal_species_names( conn: Connection ) -> list[ str ]:
   cur = conn.cursor()

   data = cur.execute(
      """   SELECT
               a.SPECIES
            FROM Animal a;
      """ )

   species_names = [
      row[ 0 ]
      for row in data.fetchall()
   ]

   cur.close()

   return species_names
