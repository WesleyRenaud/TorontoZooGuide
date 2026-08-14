from __future__ import annotations

from datetime import date

from ...shared.enums.transportation_name import TransportationName
from ...types import Connection
from .zoomobile_station_mapper import map_zoomobile_station_records
from .zoomobile_station_mapper import map_zoomobile_station_status_records
from .zoomobile_station_record import ZoomobileStationRecord
from .zoomobile_station_status_record import ZoomobileStationStatusRecord


def fetch_zoomobile_station_names( conn: Connection ) -> list[ str ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  s.NAME
               FROM TransportationStation s
               WHERE s.TRANSPORTATION = ?;
         """,
         ( TransportationName.ZOOMOBILE, ) )

      return [ row[ 0 ] for row in data.fetchall() ]

   finally:
      cur.close()


def fetch_zoomobile_station_records(
      conn: Connection ) -> list[ ZoomobileStationRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  s.NAME,
                  s.DESCRIPTION,
                  s.X_COORD,
                  s.Y_COORD
               FROM TransportationStation s
               WHERE s.TRANSPORTATION = ?;
         """,
         ( TransportationName.ZOOMOBILE, ) )

      return map_zoomobile_station_records( data.fetchall() )

   finally:
      cur.close()


def fetch_zoomobile_route_ids( conn: Connection ) -> list[ str ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  r.ROUTE
               FROM TransportationRoute r
               WHERE r.TRANSPORTATION = ?;
         """,
         ( TransportationName.ZOOMOBILE, ) )

      return [ row[ 0 ] for row in data.fetchall() ]

   finally:
      cur.close()


def fetch_zoomobile_route_station_names(
      conn: Connection,
      route: str ) -> list[ str ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  rs.STATION
               FROM TransportationRouteStation rs
               WHERE rs.TRANSPORTATION = ?
               AND rs.ROUTE = ?;
         """,
         ( TransportationName.ZOOMOBILE, route ) )

      return [ row[ 0 ] for row in data.fetchall() ]

   finally:
      cur.close()


def fetch_zoomobile_station_status_records(
      conn: Connection ) -> list[ ZoomobileStationStatusRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  s.STATION,
                  s.CLOSED_START,
                  s.CLOSED_END,
                  s.IS_CLOSED,
                  s.CLOSED_MESSAGE
               FROM TransportationStationStatus s
               WHERE s.TRANSPORTATION = ?;
         """,
         ( TransportationName.ZOOMOBILE, ) )

      return map_zoomobile_station_status_records( data.fetchall() )

   finally:
      cur.close()


def fetch_active_zoomobile_route(
      conn: Connection,
      target_date: date ) -> str | None:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  z.ROUTE
               FROM ZoomobileRouteSchedule z
               WHERE z.SCHEDULE_START_DATE <= ?
               AND (
                  z.SCHEDULE_END_DATE IS NULL
                  OR z.SCHEDULE_END_DATE >= ?
               )
               ORDER BY z.SCHEDULE_START_DATE DESC
               LIMIT 1;
         """, ( target_date.isoformat(), target_date.isoformat() ) )

      route_data = data.fetchone()

      if route_data is None:
         return None

      return route_data[ 'ROUTE' ]

   finally:
      cur.close()


def fetch_zoomobile_day_route(
      conn: Connection,
      month: int,
      day: int ) -> str | None:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  z.ROUTE
               FROM TransportationDayRoute z
               WHERE z.TRANSPORTATION = ?
               AND z.MONTH = ?
               AND z.DAY = ?;
         """, ( TransportationName.ZOOMOBILE, month, day ) )

      route_data = data.fetchone()

      if route_data is None:
         return None

      return route_data[ 'ROUTE' ]

   finally:
      cur.close()
