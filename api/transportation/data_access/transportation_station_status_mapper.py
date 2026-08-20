from __future__ import annotations

from .transportation_station_status_record import TransportationStationStatusRecord
from ...types import Row


def map_transportation_station_status_record(
      row: Row,
) -> TransportationStationStatusRecord:
   return TransportationStationStatusRecord(
      station=row[ 'STATION' ],
      closed_start=row[ 'CLOSED_START' ],
      closed_end=row[ 'CLOSED_END' ],
      is_closed=row[ 'IS_CLOSED' ],
      closed_message=row[ 'CLOSED_MESSAGE' ] )


def map_transportation_station_status_records(
      rows: list[ Row ],
) -> list[ TransportationStationStatusRecord ]:
   return [
      map_transportation_station_status_record( row )
      for row in rows
   ]
