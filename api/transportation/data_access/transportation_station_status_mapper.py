from __future__ import annotations

from .transportation_station_status_record import TransportationStationStatusRecord
from ...types import Row


class TransportationStationStatusMapper():
   @classmethod
   def map_record(
         cls,
         row: Row,
   ) -> TransportationStationStatusRecord:
      return TransportationStationStatusRecord(
         station=row[ 'STATION' ],
         closed_start=row[ 'CLOSED_START' ],
         closed_end=row[ 'CLOSED_END' ],
         is_closed=row[ 'IS_CLOSED' ],
         closed_message=row[ 'CLOSED_MESSAGE' ] )


   @classmethod
   def map_records(
         cls,
         rows: list[ Row ],
   ) -> list[ TransportationStationStatusRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
