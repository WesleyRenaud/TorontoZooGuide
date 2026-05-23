from __future__ import annotations

from ...types import Connection
from ..logic.zoomobile_station_closed_status import ZoomobileStationClosedStatus


def save_zoomobile_station_closed_status(
      conn: Connection,
      status: ZoomobileStationClosedStatus ) -> bool:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO ZoomobileStationStatus (
                  ZOOMOBILE_STATION,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, 1, ?, ?, ?)
               ON CONFLICT(ZOOMOBILE_STATION) DO UPDATE SET
                  IS_CLOSED = 1,
                  CLOSED_MESSAGE = excluded.CLOSED_MESSAGE,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """,
         (
            status.zoomobile_station,
            status.message,
            status.start_date,
            status.end_date,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()



def save_zoomobile_station_open_status(
      conn: Connection,
      zoomobile_station: str ) -> bool:
   cur = conn.cursor()

   try:
      cur.execute(
         """   DELETE FROM ZoomobileStationStatus
               WHERE ZOOMOBILE_STATION = ?;
         """,
         ( zoomobile_station, ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
