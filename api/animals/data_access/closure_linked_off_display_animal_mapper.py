from __future__ import annotations

from ..domain.closure_linked_off_display_animal import ClosureLinkedOffDisplayAnimal
from ...shared.date_values import DateValues
from ...types import Types


class ClosureLinkedOffDisplayAnimalMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> ClosureLinkedOffDisplayAnimal:
      return ClosureLinkedOffDisplayAnimal(
         species=row[ 'SPECIES' ],
         exhibit=row[ 'EXHIBIT' ],
         end=DateValues.parse_date_value( row[ 'OFF_DISPLAY_END' ] ),
         closure_update_title=row[ 'CLOSURE_UPDATE_TITLE' ],
         closure_update_start=DateValues.parse_date_value( row[ 'CLOSURE_UPDATE_START' ] ) )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ ClosureLinkedOffDisplayAnimal ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
