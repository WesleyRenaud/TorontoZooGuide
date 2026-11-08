from __future__ import annotations

from ..domain.temporary_off_display_animal import TemporaryOffDisplayAnimal
from ...shared.date_values import DateValues
from ...types import Types


class TemporaryOffDisplayAnimalMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> TemporaryOffDisplayAnimal:
      return TemporaryOffDisplayAnimal(
         species=row[ 'SPECIES' ],
         exhibit=row[ 'EXHIBIT' ],
         viewing_scope=row[ 'VIEWING_SCOPE' ],
         start=DateValues.parse_date_value( row[ 'OFF_DISPLAY_START' ] ),
         end=DateValues.parse_date_value( row[ 'OFF_DISPLAY_END' ] ),
         closure_update_title=row[ 'CLOSURE_UPDATE_TITLE' ],
         closure_update_start=DateValues.parse_date_value( row[ 'CLOSURE_UPDATE_START' ] ) )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ TemporaryOffDisplayAnimal ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
