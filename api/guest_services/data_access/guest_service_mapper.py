from __future__ import annotations

from collections.abc import Iterable

from ... import zoo
from ...types import Row


def map_guest_service_record( row: Row ) -> zoo.GuestService:
   return zoo.GuestService(
      service_type=row[ 'SERVICE_TYPE' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_guest_service_records( rows: Iterable[ Row ] ) -> list[ zoo.GuestService ]:
   return [
      map_guest_service_record( row )
      for row in rows
   ]
