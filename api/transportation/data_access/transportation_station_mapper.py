from __future__ import annotations

from .transportation_station_record import TransportationStationRecord
from ...types import Row


class TransportationStationMapper():
   @classmethod
   def map_record( cls, row: Row ) -> TransportationStationRecord:
      return TransportationStationRecord(
         name=row[ 'NAME' ],
         description=row[ 'DESCRIPTION' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ] )


   @classmethod
   def map_records(
         cls,
         rows: list[ Row ],
   ) -> list[ TransportationStationRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
