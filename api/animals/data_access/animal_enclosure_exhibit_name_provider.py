from __future__ import annotations

from .animal_species_exhibit_mapper import AnimalSpeciesExhibitMapper
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


   @classmethod
   def fetch_animal_species_exhibits( cls, conn: Types.Connection ) -> list[ AnimalSpeciesExhibit ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     SPECIES,
                     EXHIBIT
                  FROM Enclosure
                  ORDER BY SPECIES, EXHIBIT;
            """ )

         return AnimalSpeciesExhibitMapper.map_records( data.fetchall() )

      finally:
         cur.close()
