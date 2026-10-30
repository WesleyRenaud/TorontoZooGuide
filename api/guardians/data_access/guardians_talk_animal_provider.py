from __future__ import annotations

from ...animals.search.species_exhibit_key import SpeciesExhibitKey
from .guardians_talk_animal_record import GuardiansTalkAnimalRecord
from .guardians_talk_animal_record_mapper import GuardiansTalkAnimalRecordMapper
from ...types import Types


class GuardiansTalkAnimalProvider():
   @classmethod
   def fetch_linked_animals(
         cls,
         conn: Types.Connection,
         talk_name: str,
         *,
         location: str | None = None,
         enclosure_name: str | None = None ) -> list[ SpeciesExhibitKey ]:
      return [
         link.species_exhibit_key()
         for link in cls.fetch_animal_links(
            conn,
            talk_name,
            location=location,
            enclosure_name=enclosure_name )
      ]


   @classmethod
   def fetch_animal_links(
         cls,
         conn: Types.Connection,
         talk_name: str,
         *,
         location: str | None = None,
         enclosure_name: str | None = None ) -> list[ GuardiansTalkAnimalRecord ]:
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
                  WHERE TALK_NAME = ?
                  AND ( ? IS NULL OR LOCATION = ? )
                  AND ( ? IS NULL OR ENCLOSURE_NAME IS ? );
            """,
            (
               talk_name,
               location,
               location,
               enclosure_name,
               enclosure_name,
            ) )

         return GuardiansTalkAnimalRecordMapper.map_records( data.fetchall() )

      finally:
         cur.close()
