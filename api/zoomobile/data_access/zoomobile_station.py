from .zoomobile_station_mapper import map_zoomobile_station_records
from .zoomobile_station_mapper import map_zoomobile_station_status_records


def fetch_zoomobile_station_names( conn ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  s.NAME
               FROM ZoomobileStation s;
         """ )

      return [ row[ 0 ] for row in data.fetchall() ]

   finally:
      cur.close()


def fetch_zoomobile_station_records( conn ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  s.NAME,
                  s.ON_WINTER_ROUTE,
                  s.DESCRIPTION,
                  s.X_COORD,
                  s.Y_COORD
               FROM ZoomobileStation s;
         """ )

      return map_zoomobile_station_records( data.fetchall() )

   finally:
      cur.close()


def fetch_zoomobile_station_status_records( conn ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  s.ZOOMOBILE_STATION,
                  s.CLOSED_START,
                  s.CLOSED_END,
                  s.IS_CLOSED,
                  s.CLOSED_MESSAGE
               FROM ZoomobileStationStatus s;
         """ )

      return map_zoomobile_station_status_records( data.fetchall() )

   finally:
      cur.close()


def fetch_active_zoomobile_route( conn, target_date ):
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


def fetch_zoomobile_day_route( conn, month, day ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  z.ROUTE
               FROM ZoomobileDayRoute z
               WHERE z.MONTH = ?
               AND z.DAY = ?;
         """, ( month, day ) )

      route_data = data.fetchone()

      if route_data is None:
         return None

      return route_data[ 'ROUTE' ]

   finally:
      cur.close()
