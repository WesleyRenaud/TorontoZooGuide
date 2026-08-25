from __future__ import annotations

from ..status.station_closed_status import TransportationStationClosedStatus
from ...types import Connection


def save_transportation_station_closed_status(
      conn: Connection,
      transportation: str,
      status: TransportationStationClosedStatus ) -> bool:
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
            transportation,
            status.transportation_station,
            status.message,
            status.start_date,
            status.end_date,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def save_transportation_station_open_status(
      conn: Connection,
      transportation: str,
      transportation_station: str ) -> bool:
   cur = conn.cursor()

   try:
      cur.execute(
         """   DELETE FROM TransportationStationStatus
               WHERE TRANSPORTATION = ?
               AND STATION = ?;
         """,
         ( transportation, transportation_station ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
