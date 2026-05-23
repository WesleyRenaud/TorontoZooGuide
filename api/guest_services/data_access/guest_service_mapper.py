from __future__ import annotations

from collections.abc import Iterable

from ...models import GuestService
from ...types import Row


def map_guest_service_record( row: Row ) -> GuestService:
   return GuestService(
      service_type=row[ 'SERVICE_TYPE' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_guest_service_records( rows: Iterable[ Row ] ) -> list[ GuestService ]:
   return [
      map_guest_service_record( row )
      for row in rows
   ]
