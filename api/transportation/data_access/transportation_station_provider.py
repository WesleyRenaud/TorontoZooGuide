from __future__ import annotations

from .transportation_station_mapper import TransportationStationMapper
from .transportation_station_record import TransportationStationRecord
from ...types import Types


class TransportationStationProvider():
   @classmethod
   def fetch_transportation_station_names(
         cls,
         conn: Types.Connection,
         transportation: str,
   ) -> list[ str ]:
      cur = conn.cursor()
      try:
         rows = cur.execute(
            """   SELECT
                     s.NAME
                  FROM TransportationStation s
                  WHERE s.TRANSPORTATION = ?;
            """,
            ( transportation, ),
         ).fetchall()
         return [ row[ 0 ] for row in rows ]
      finally:
         cur.close()


   @classmethod
   def fetch_transportation_station_records(
         cls,
         conn: Types.Connection,
         transportation: str,
   ) -> list[ TransportationStationRecord ]:
      cur = conn.cursor()
      try:
         rows = cur.execute(
            """   SELECT
                     s.NAME,
                     s.DESCRIPTION,
                     s.X_COORD,
                     s.Y_COORD
                  FROM TransportationStation s
                  WHERE s.TRANSPORTATION = ?;
            """,
            ( transportation, ),
         ).fetchall()
         return TransportationStationMapper.map_records( rows )
      finally:
         cur.close()


   @classmethod
   def fetch_main_transportation_station_record(
         cls,
         conn: Types.Connection,
         transportation: str,
   ) -> TransportationStationRecord | None:
      cur = conn.cursor()
      try:
         row = cur.execute(
            """   SELECT
                     s.NAME,
                     s.DESCRIPTION,
                     s.X_COORD,
                     s.Y_COORD
                  FROM TransportationStation s
                  WHERE s.TRANSPORTATION = ?
                    AND s.IS_MAIN_STATION = 1;
            """,
            ( transportation, ),
         ).fetchone()
         if row is None:
            return None
         return TransportationStationMapper.map_record( row )
      finally:
         cur.close()


   @classmethod
   def fetch_transportation_station_record(
         cls,
         conn: Types.Connection,
         transportation: str,
         station_name: str,
   ) -> TransportationStationRecord | None:
      cur = conn.cursor()
      try:
         row = cur.execute(
            """   SELECT
                     s.NAME,
                     s.DESCRIPTION,
                     s.X_COORD,
                     s.Y_COORD
                  FROM TransportationStation s
                  WHERE s.TRANSPORTATION = ?
                    AND s.NAME = ?;
            """,
            ( transportation, station_name ),
         ).fetchone()
         if row is None:
            return None
         return TransportationStationMapper.map_record( row )
      finally:
         cur.close()
