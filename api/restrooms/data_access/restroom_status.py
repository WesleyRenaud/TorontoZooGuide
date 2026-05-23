from __future__ import annotations

from ...types import Connection, DateInput


def save_restroom_closed_status(
      conn: Connection,
      restroom: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> bool:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO RestroomStatus (
                  RESTROOM,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, 1, ?, ?, ?)
               ON CONFLICT(RESTROOM) DO UPDATE SET
                  IS_CLOSED = 1,
                  CLOSED_MESSAGE = excluded.CLOSED_MESSAGE,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """,
         (
            restroom,
            message,
            start_date,
            end_date,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def save_restroom_open_status(
      conn: Connection,
      restroom: str,
      start_date: DateInput,
      end_date: DateInput ) -> bool:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO RestroomStatus (
                  RESTROOM,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, 0, NULL, ?, ?)
               ON CONFLICT(RESTROOM) DO UPDATE SET
                  IS_CLOSED = 0,
                  CLOSED_MESSAGE = NULL,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """,
         (
            restroom,
            start_date,
            end_date,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
