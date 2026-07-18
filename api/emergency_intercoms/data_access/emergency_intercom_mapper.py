from __future__ import annotations

from ...models import EmergencyIntercom
from ...types import Row


def map_emergency_intercom_record( row: Row ) -> EmergencyIntercom:
   return EmergencyIntercom(
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_emergency_intercom_records( rows: list[ Row ] ) -> list[ EmergencyIntercom ]:
   return [
      map_emergency_intercom_record( row )
      for row in rows
   ]
