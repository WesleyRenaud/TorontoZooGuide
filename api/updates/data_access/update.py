from .update_mapper import map_update_records


def insert_update( conn, update ):
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO ZooUpdate (
                  TITLE,
                  DESCRIPTION,
                  UPDATE_TYPE,
                  START_DATE,
                  END_DATE
               )
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(TITLE, START_DATE) DO NOTHING;
         """,
         (
            update.title,
            update.description,
            update.update_type,
            update.start_date,
            update.end_date or None,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def update_end_date( conn, update ):
   cur = conn.cursor()

   try:
      cur.execute(
         """   UPDATE ZooUpdate
               SET END_DATE = ?
               WHERE TITLE = ?
                  AND START_DATE = ?;
         """,
         (
            update.end_date,
            update.title,
            update.start_date,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def edit_update_record( conn, update ):
   cur = conn.cursor()

   try:
      cur.execute(
         """  UPDATE ZooUpdate
               SET DESCRIPTION = ?,
                   UPDATE_TYPE = ?,
                   END_DATE = ?
               WHERE TITLE = ?
                  AND START_DATE = ?;
         """,
         (
            update.description,
            update.update_type,
            update.end_date,
            update.title,
            update.start_date,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def fetch_updates( conn, as_of_date ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  TITLE,
                  DESCRIPTION,
                  UPDATE_TYPE,
                  START_DATE,
                  END_DATE
               FROM ZooUpdate
               WHERE END_DATE IS NULL
                  OR END_DATE >= ?
               ORDER BY START_DATE DESC, TITLE ASC;
         """,
         ( as_of_date, ) )

      return map_update_records( data.fetchall() )

   finally:
      cur.close()
