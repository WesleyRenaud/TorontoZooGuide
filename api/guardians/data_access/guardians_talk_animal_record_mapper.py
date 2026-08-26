from __future__ import annotations

from .guardians_talk_animal_record import GuardiansTalkAnimalRecord
from ...types import Row


class GuardiansTalkAnimalRecordMapper():
   @classmethod
   def map_record( cls, row: Row ) -> GuardiansTalkAnimalRecord:
      return GuardiansTalkAnimalRecord(
         talk_name=row[ 'TALK_NAME' ],
         location=row[ 'LOCATION' ],
         species=row[ 'SPECIES' ],
         exhibit=row[ 'EXHIBIT' ],
         enclosure_name=row[ 'ENCLOSURE_NAME' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ GuardiansTalkAnimalRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
