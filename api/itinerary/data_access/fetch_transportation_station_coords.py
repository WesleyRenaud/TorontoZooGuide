from __future__ import annotations

from ..domain.transportation_station_coords import TransportationStationCoords
from ...request_connection import get_connection
from .transportation_station_coords_mapper import map_transportation_station_coords


def fetch_transportation_station_coords(
      transportation: str,
      station_name: str ) -> TransportationStationCoords | None:
   conn = get_connection()
   cur = conn.cursor()

   try:
      row = cur.execute(
         """   SELECT NAME, X_COORD, Y_COORD
               FROM TransportationStation
               WHERE TRANSPORTATION = ?
                 AND NAME = ?;
         """,
         ( transportation, station_name ),
      ).fetchone()

      if row is None:
         return None

      return map_transportation_station_coords( row )

   finally:
      cur.close()
