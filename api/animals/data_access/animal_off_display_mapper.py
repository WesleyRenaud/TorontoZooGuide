from __future__ import annotations

from .animal_off_display_record import AnimalOffDisplayRecord
from ...types import Types


class AnimalOffDisplayMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> AnimalOffDisplayRecord:
      return AnimalOffDisplayRecord(
         species=row[ 'SPECIES' ],
         is_off_display=bool( row[ 'IS_OFF_DISPLAY' ] ),
         start=row[ 'OFF_DISPLAY_START' ],
         end=row[ 'OFF_DISPLAY_END' ],
         off_for_season=bool( row[ 'OFF_DISPLAY_FOR_SEASON' ] ) )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ AnimalOffDisplayRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
