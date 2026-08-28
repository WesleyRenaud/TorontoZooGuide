from __future__ import annotations

from ...types import Types


class RestroomAlertProvider():
   @classmethod
   def save_alert(
         cls,
         conn: Types.Connection,
         restroom: str,
         alert_start_date: Types.DateInput,
         alert_end_date: Types.DateInput,
         message: str ) -> bool:
      cur = conn.cursor()

      try:
         cls._clear_with_cursor(
            cur,
            restroom=restroom )
         cls._insert_with_cursor(
            cur,
            restroom=restroom,
            alert_start_date=alert_start_date,
            alert_end_date=alert_end_date,
            message=message )
         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def delete_alert( cls, conn: Types.Connection, restroom: str ) -> bool:
      cur = conn.cursor()

      try:
         cls._clear_with_cursor(
            cur,
            restroom=restroom )
         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def _clear_with_cursor(
         cls,
         cur: Types.Cursor,
         restroom: str ) -> None:
      cur.execute(
         """ DELETE FROM RestroomAlert
             WHERE RESTROOM = ?;
         """,
         ( restroom, ) )


   @classmethod
   def _insert_with_cursor(
         cls,
         cur: Types.Cursor,
         restroom: str,
         alert_start_date: Types.DateInput,
         alert_end_date: Types.DateInput,
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
