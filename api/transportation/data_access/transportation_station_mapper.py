from __future__ import annotations

from .transportation_station_record import TransportationStationRecord
from ...types import Row


def map_transportation_station_record( row: Row ) -> TransportationStationRecord:
   return TransportationStationRecord(
      name=row[ 'NAME' ],
      description=row[ 'DESCRIPTION' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )


def map_transportation_station_records(
      rows: list[ Row ],
) -> list[ TransportationStationRecord ]:
   return [
      map_transportation_station_record( row )
      for row in rows
   ]
