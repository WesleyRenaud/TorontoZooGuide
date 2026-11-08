from __future__ import annotations

from ..domain.enclosure_off_display_status import EnclosureOffDisplayStatus
from ...shared.date_values import DateValues
from ...types import Types


class EnclosureOffDisplayStatusMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> EnclosureOffDisplayStatus:
      return EnclosureOffDisplayStatus(
         species=row[ 'SPECIES' ],
         exhibit=row[ 'EXHIBIT' ],
         start=DateValues.parse_date_value( row[ 'OFF_DISPLAY_START' ] ),
         end=DateValues.parse_date_value( row[ 'OFF_DISPLAY_END' ] ) )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ EnclosureOffDisplayStatus ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
