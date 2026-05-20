from .exhibit_closure_mapper import map_exhibit_closure_records


def save_exhibit_closed_status(
      conn,
      exhibit,
      start_date,
      end_date,
      message ):
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO ExhibitStatus (
                  EXHIBIT,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, 1, ?, ?, ?)
               ON CONFLICT(EXHIBIT) DO UPDATE SET
                  IS_CLOSED = 1,
                  CLOSED_MESSAGE = excluded.CLOSED_MESSAGE,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """,
         (
            exhibit,
            message,
            start_date,
            end_date,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def save_exhibit_open_status(
      conn,
      exhibit,
      start_date,
      end_date ):
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO ExhibitStatus (
                  EXHIBIT,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, 0, NULL, ?, ?)
               ON CONFLICT(EXHIBIT) DO UPDATE SET
                  IS_CLOSED = 0,
                  CLOSED_MESSAGE = NULL,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """,
         (
            exhibit,
            start_date,
            end_date,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def fetch_exhibit_closure_records( conn ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  EXHIBIT,
                  CLOSED_START,
                  CLOSED_END
               FROM ExhibitStatus
               WHERE IS_CLOSED = 1;
         """ )

      return map_exhibit_closure_records( data.fetchall() )

   finally:
      cur.close()
