from __future__ import annotations

from ...models import EmergencyIntercom
from ...types import Row


class EmergencyIntercomMapper():
   @classmethod
   def map_record( cls, row: Row ) -> EmergencyIntercom:
      return EmergencyIntercom(
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ EmergencyIntercom ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
