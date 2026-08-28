from __future__ import annotations

from .attraction_animal_record import AttractionAnimalRecord
from ...types import Types


class AttractionAnimalMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> AttractionAnimalRecord:
      return AttractionAnimalRecord(
         attraction=row[ 'ATTRACTION' ],
         species=row[ 'SPECIES' ],
         exhibit=row[ 'EXHIBIT' ],
         enclosure_name=row[ 'ENCLOSURE_NAME' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ AttractionAnimalRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
