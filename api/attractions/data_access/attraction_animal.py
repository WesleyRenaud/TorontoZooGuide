from __future__ import annotations

from ...animals.search.species_exhibit_key import SpeciesExhibitKey
from .attraction_animal_record import AttractionAnimalRecord
from .attraction_animal_record_mapper import map_attraction_animal_records
from ...types import Connection


def fetch_attraction_linked_animals(
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
         SpeciesExhibitKey.from_values(
            row[ 'SPECIES' ],
            row[ 'EXHIBIT' ] )
         for row in data.fetchall()
      ]

   finally:
      cur.close()


def fetch_attraction_animal_links(
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

      return map_attraction_animal_records( data.fetchall() )

   finally:
      cur.close()
