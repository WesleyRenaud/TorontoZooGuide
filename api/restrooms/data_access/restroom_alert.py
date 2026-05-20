def save_restroom_alert(
      conn,
      restroom,
      alert_start_date,
      alert_end_date,
      message ):
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


def clear_restroom_alert_with_cursor( cur, restroom ):
   cur.execute(
      """ DELETE FROM RestroomAlert
          WHERE RESTROOM = ?;
      """,
      ( restroom, ) )


def delete_restroom_alert( conn, restroom ):
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
      cur,
      restroom,
      alert_start_date,
      alert_end_date,
      message ):
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
