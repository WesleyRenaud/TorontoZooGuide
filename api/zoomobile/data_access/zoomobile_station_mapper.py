from __future__ import annotations

from ...types import Row
from .zoomobile_station_record import ZoomobileStationRecord
from .zoomobile_station_status_record import ZoomobileStationStatusRecord


def map_zoomobile_station_record( row: Row ) -> ZoomobileStationRecord:
   return ZoomobileStationRecord(
      name=row[ 'NAME' ],
      description=row[ 'DESCRIPTION' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )


def map_zoomobile_station_records( rows: list[ Row ] ) -> list[ ZoomobileStationRecord ]:
   return [
      map_zoomobile_station_record( row )
      for row in rows
   ]


def map_zoomobile_station_status_record( row: Row ) -> ZoomobileStationStatusRecord:
   return ZoomobileStationStatusRecord(
      station=row[ 'STATION' ],
      closed_start=row[ 'CLOSED_START' ],
      closed_end=row[ 'CLOSED_END' ],
      is_closed=row[ 'IS_CLOSED' ],
      closed_message=row[ 'CLOSED_MESSAGE' ] )


def map_zoomobile_station_status_records( rows: list[ Row ] ) -> list[ ZoomobileStationStatusRecord ]:
   return [
      map_zoomobile_station_status_record( row )
      for row in rows
   ]
