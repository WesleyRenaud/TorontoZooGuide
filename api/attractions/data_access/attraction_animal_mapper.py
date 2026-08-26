from __future__ import annotations

from .attraction_animal_record import AttractionAnimalRecord
from ...types import Row


class AttractionAnimalMapper():
   @classmethod
   def map_record( cls, row: Row ) -> AttractionAnimalRecord:
      return AttractionAnimalRecord(
         attraction=row[ 'ATTRACTION' ],
         species=row[ 'SPECIES' ],
         exhibit=row[ 'EXHIBIT' ],
         enclosure_name=row[ 'ENCLOSURE_NAME' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ AttractionAnimalRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
