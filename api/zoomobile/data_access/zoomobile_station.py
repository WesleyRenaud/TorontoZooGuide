from __future__ import annotations

from datetime import date

from ...shared.enums.transportation_name import TransportationName
from ...transportation.data_access.transportation_station import fetch_transportation_station_names
from ...transportation.data_access.transportation_station import fetch_transportation_station_records
from ...transportation.data_access.transportation_station import fetch_transportation_station_status_records
from ...transportation.data_access.transportation_station_record import TransportationStationRecord
from ...transportation.data_access.transportation_station_status_record import TransportationStationStatusRecord
from ...types import Connection


def fetch_zoomobile_station_names( conn: Connection ) -> list[ str ]:
   return fetch_transportation_station_names(
      conn,
      TransportationName.ZOOMOBILE )


def fetch_zoomobile_station_records(
      conn: Connection ) -> list[ TransportationStationRecord ]:
   return fetch_transportation_station_records(
      conn,
      TransportationName.ZOOMOBILE )


def fetch_zoomobile_station_status_records(
      conn: Connection ) -> list[ TransportationStationStatusRecord ]:
   return fetch_transportation_station_status_records(
      conn,
      TransportationName.ZOOMOBILE )


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


def fetch_active_zoomobile_route(
      conn: Connection,
      target_date: date ) -> str | None:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  ROUTE
               FROM TransportationRouteSchedule
               WHERE TRANSPORTATION = ?
                 AND SCHEDULE_START_DATE <= ?
               AND (
                  SCHEDULE_END_DATE IS NULL
                  OR SCHEDULE_END_DATE >= ?
               )
               ORDER BY SCHEDULE_START_DATE DESC
               LIMIT 1;
         """,
         (
            TransportationName.ZOOMOBILE,
            target_date.isoformat(),
            target_date.isoformat(),
         ) )

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
