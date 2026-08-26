from __future__ import annotations

from ...animals.search.species_exhibit_key import SpeciesExhibitKey
from .attraction_animal_mapper import AttractionAnimalMapper
from .attraction_animal_record import AttractionAnimalRecord
from ...types import Connection


class AttractionAnimalProvider():
   @classmethod
   def fetch_attraction_linked_animals(
         cls,
         conn: Connection,
         attraction_name: str ) -> list[ SpeciesExhibitKey ]:
      cur = conn.cursor()
      try:
         data = cur.execute(
            """   SELECT
                     SPECIES,
                     EXHIBIT
                  FROM AttractionAnimal
                  WHERE ATTRACTION = ?;
            """,
            ( attraction_name, ) )
         return [
            SpeciesExhibitKey.from_values( row[ 'SPECIES' ], row[ 'EXHIBIT' ] )
            for row in data.fetchall()
         ]
      finally:
         cur.close()


   @classmethod
   def fetch_attraction_animal_links(
         cls,
         conn: Connection,
         attraction_name: str ) -> list[ AttractionAnimalRecord ]:
      cur = conn.cursor()
      try:
         data = cur.execute(
            """   SELECT
                     ATTRACTION,
                     SPECIES,
                     EXHIBIT,
                     ENCLOSURE_NAME
                  FROM AttractionAnimal
                  WHERE ATTRACTION = ?;
            """,
            ( attraction_name, ) )
         return AttractionAnimalMapper.map_records( data.fetchall() )
      finally:
         cur.close()
