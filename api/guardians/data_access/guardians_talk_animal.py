from __future__ import annotations

from ...animals.search.species_exhibit_key import SpeciesExhibitKey
from .guardians_talk_animal_mapper import map_guardians_talk_linked_animals
from ...types import Connection


def fetch_guardians_talk_linked_animals(
      conn: Connection,
      talk_name: str ) -> list[ SpeciesExhibitKey ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  SPECIES,
                  EXHIBIT
               FROM GuardiansTalkAnimal
               WHERE TALK_NAME = ?;
         """,
         ( talk_name, ) )

      return map_guardians_talk_linked_animals( data.fetchall() )

   finally:
      cur.close()
