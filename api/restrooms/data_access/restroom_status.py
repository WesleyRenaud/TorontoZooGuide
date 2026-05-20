def save_restroom_closed_status(
      conn,
      restroom,
      start_date,
      end_date,
      message ):
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
      conn,
      restroom,
      start_date,
      end_date ):
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
