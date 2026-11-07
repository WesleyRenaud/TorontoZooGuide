from __future__ import annotations

from ..domain.enclosure_off_display_month import EnclosureOffDisplayMonth
from ...types import Types


class EnclosureOffDisplayMonthMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> EnclosureOffDisplayMonth:
      return EnclosureOffDisplayMonth(
         species=row[ 'SPECIES' ],
         exhibit=row[ 'EXHIBIT' ],
         until_month=row[ 'OFF_DISPLAY_FOR_SEASON_UNTIL_MONTH' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ EnclosureOffDisplayMonth ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
