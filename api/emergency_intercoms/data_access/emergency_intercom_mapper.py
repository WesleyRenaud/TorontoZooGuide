from __future__ import annotations

from collections.abc import Iterable

from ... import zoo
from ...types import Row


def map_emergency_intercom_record( row: Row ) -> zoo.EmergencyIntercom:
   return zoo.EmergencyIntercom(
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_emergency_intercom_records( rows: Iterable[ Row ] ) -> list[ zoo.EmergencyIntercom ]:
   return [
      map_emergency_intercom_record( row )
      for row in rows
   ]
