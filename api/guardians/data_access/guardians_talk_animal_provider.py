from __future__ import annotations

from ...animals.search.species_exhibit_key import SpeciesExhibitKey
from .guardians_talk_animal_mapper import GuardiansTalkAnimalMapper
from .guardians_talk_animal_record import GuardiansTalkAnimalRecord
from .guardians_talk_animal_record_mapper import GuardiansTalkAnimalRecordMapper
from ...types import Connection


class GuardiansTalkAnimalProvider():
   @classmethod
   def fetch_linked_animals(
         cls,
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

         return GuardiansTalkAnimalMapper.map_linked_animals( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def fetch_animal_links(
         cls,
         conn: Connection,
         talk_name: str ) -> list[ GuardiansTalkAnimalRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     TALK_NAME,
                     LOCATION,
                     SPECIES,
                     EXHIBIT,
                     ENCLOSURE_NAME
                  FROM GuardiansTalkAnimal
                  WHERE TALK_NAME = ?;
            """,
            ( talk_name, ) )

         return GuardiansTalkAnimalRecordMapper.map_records( data.fetchall() )

      finally:
         cur.close()
