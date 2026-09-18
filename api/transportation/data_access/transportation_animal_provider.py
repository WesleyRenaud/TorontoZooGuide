from __future__ import annotations

from .transportation_animal_mapper import TransportationAnimalMapper
from .transportation_animal_record import TransportationAnimalRecord
from ...types import Types


class TransportationAnimalProvider():
   @classmethod
   def fetch_all( cls, conn: Types.Connection ) -> list[ TransportationAnimalRecord ]:
      cur = conn.cursor()

      try:
         rows = cur.execute(
            """   SELECT
                     TRANSPORTATION,
                     FROM_STATION,
                     TO_STATION,
                     SPECIES,
                     EXHIBIT,
                     ENCLOSURE_NAME
                  FROM TransportationAnimal;
            """
         ).fetchall()
      finally:
         cur.close()

      return TransportationAnimalMapper.map_records( rows )
