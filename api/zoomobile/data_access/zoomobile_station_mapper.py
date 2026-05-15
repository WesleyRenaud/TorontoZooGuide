from .zoomobile_station_record import ZoomobileStationRecord
from .zoomobile_station_status_record import ZoomobileStationStatusRecord


def map_zoomobile_station_record( row ):
   return ZoomobileStationRecord(
      name=row[ 'NAME' ],
      on_winter_route=row[ 'ON_WINTER_ROUTE' ],
      description=row[ 'DESCRIPTION' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )


def map_zoomobile_station_records( rows ):
   return [
      map_zoomobile_station_record( row )
      for row in rows
   ]


def map_zoomobile_station_status_record( row ):
   return ZoomobileStationStatusRecord(
      zoomobile_station=row[ 'ZOOMOBILE_STATION' ],
      closed_start=row[ 'CLOSED_START' ],
      closed_end=row[ 'CLOSED_END' ],
      is_closed=row[ 'IS_CLOSED' ],
      closed_message=row[ 'CLOSED_MESSAGE' ] )


def map_zoomobile_station_status_records( rows ):
   return [
      map_zoomobile_station_status_record( row )
      for row in rows
   ]
