from __future__ import annotations

from .transportation_station_mapper import map_transportation_station_record
from .transportation_station_mapper import map_transportation_station_records
from .transportation_station_record import TransportationStationRecord
from .transportation_station_status_mapper import map_transportation_station_status_records
from .transportation_station_status_record import TransportationStationStatusRecord
from ...types import Connection


def fetch_transportation_station_names(
      conn: Connection,
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


def fetch_transportation_station_records(
      conn: Connection,
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

      return map_transportation_station_records( rows )

   finally:
      cur.close()


def fetch_transportation_station_status_records(
      conn: Connection,
      transportation: str,
) -> list[ TransportationStationStatusRecord ]:
   cur = conn.cursor()

   try:
      rows = cur.execute(
         """   SELECT
                  s.STATION,
                  s.CLOSED_START,
                  s.CLOSED_END,
                  s.IS_CLOSED,
                  s.CLOSED_MESSAGE
               FROM TransportationStationStatus s
               WHERE s.TRANSPORTATION = ?;
         """,
         ( transportation, ),
      ).fetchall()

      return map_transportation_station_status_records( rows )

   finally:
      cur.close()


def fetch_main_transportation_station_record(
      conn: Connection,
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

      return map_transportation_station_record( row )

   finally:
      cur.close()


def fetch_transportation_station_record(
      conn: Connection,
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

      return map_transportation_station_record( row )

   finally:
      cur.close()
