from __future__ import annotations

from ...shared.enums.transportation_name import TransportationName
from ..status.zoomobile_station_closed_status import ZoomobileStationClosedStatus
from ...types import Connection


def save_zoomobile_station_closed_status(
      conn: Connection,
      status: ZoomobileStationClosedStatus ) -> bool:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO TransportationStationStatus (
                  TRANSPORTATION,
                  STATION,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, ?, 1, ?, ?, ?)
               ON CONFLICT(TRANSPORTATION, STATION) DO UPDATE SET
                  IS_CLOSED = 1,
                  CLOSED_MESSAGE = excluded.CLOSED_MESSAGE,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """,
         (
            TransportationName.ZOOMOBILE,
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
         """   DELETE FROM TransportationStationStatus
               WHERE TRANSPORTATION = ?
               AND STATION = ?;
         """,
         ( TransportationName.ZOOMOBILE, zoomobile_station ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
