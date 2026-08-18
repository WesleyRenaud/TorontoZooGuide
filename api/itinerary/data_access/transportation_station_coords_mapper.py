from __future__ import annotations

from ..domain.transportation_station_coords import TransportationStationCoords
from ...types import Row


def map_transportation_station_coords(
      row: Row ) -> TransportationStationCoords:
   return TransportationStationCoords(
      name=row[ 'NAME' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )
