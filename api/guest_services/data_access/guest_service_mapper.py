from __future__ import annotations

from ...models import GuestService
from ...types import Row


class GuestServiceMapper():
   @classmethod
   def map_record( cls, row: Row ) -> GuestService:
      return GuestService(
         service_type=row[ 'SERVICE_TYPE' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ GuestService ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
