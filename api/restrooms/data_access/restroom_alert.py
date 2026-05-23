from __future__ import annotations

from ...types import Connection, Cursor, DateInput


def save_restroom_alert(
      conn: Connection,
      restroom: str,
      alert_start_date: DateInput,
      alert_end_date: DateInput,
      message: str ) -> bool:
   cur = conn.cursor()

   try:
      clear_restroom_alert_with_cursor(
         cur,
         restroom=restroom )
      insert_restroom_alert_with_cursor(
         cur,
         restroom=restroom,
         alert_start_date=alert_start_date,
         alert_end_date=alert_end_date,
         message=message )
      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def clear_restroom_alert_with_cursor(
      cur: Cursor,
      restroom: str ) -> None:
   cur.execute(
      """ DELETE FROM RestroomAlert
          WHERE RESTROOM = ?;
      """,
      ( restroom, ) )


def delete_restroom_alert( conn: Connection, restroom: str ) -> bool:
   cur = conn.cursor()

   try:
      clear_restroom_alert_with_cursor(
         cur,
         restroom=restroom )
      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def insert_restroom_alert_with_cursor(
      cur: Cursor,
      restroom: str,
      alert_start_date: DateInput,
      alert_end_date: DateInput,
      message: str ) -> None:
   cur.execute(
      """   INSERT INTO RestroomAlert (
               RESTROOM,
               ALERT_MESSAGE,
               ALERT_START_DATE,
               ALERT_END_DATE
            )
            VALUES (?, ?, ?, ?)
      """,
      (
         restroom,
         message,
         alert_start_date,
         alert_end_date,
      ) )
