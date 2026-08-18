from __future__ import annotations

from ..domain.transportation_station_coords import TransportationStationCoords
from ...request_connection import get_connection
from .transportation_station_coords_mapper import map_transportation_station_coords


def fetch_main_station_coords(
      transportation: str ) -> TransportationStationCoords | None:
   conn = get_connection()
   cur = conn.cursor()

   try:
      row = cur.execute(
         """   SELECT NAME, X_COORD, Y_COORD
               FROM TransportationStation
               WHERE TRANSPORTATION = ?
                 AND IS_MAIN_STATION = 1;
         """,
         ( transportation, ),
      ).fetchone()

      if row is None:
         return None

      return map_transportation_station_coords( row )

   finally:
      cur.close()
