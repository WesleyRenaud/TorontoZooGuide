def save_animal_off_display_status(
      conn,
      species,
      exhibit,
      start_date,
      end_date,
      message ):
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO AnimalStatus (
                  SPECIES,
                  EXHIBIT,
                  IS_OFF_DISPLAY,
                  OFF_DISPLAY_START,
                  OFF_DISPLAY_END,
                  OFF_DISPLAY_MESSAGE
               )
               VALUES (?, ?, 1, ?, ?, ?)
               ON CONFLICT(SPECIES, EXHIBIT) DO UPDATE SET
                  IS_OFF_DISPLAY = 1,
                  OFF_DISPLAY_START = excluded.OFF_DISPLAY_START,
                  OFF_DISPLAY_END = excluded.OFF_DISPLAY_END,
                  OFF_DISPLAY_MESSAGE = excluded.OFF_DISPLAY_MESSAGE;
         """,
         (
            species,
            exhibit,
            start_date,
            end_date,
            message,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def save_animal_on_display_status( conn, species, exhibit ):
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO AnimalStatus (
                  SPECIES,
                  EXHIBIT,
                  IS_OFF_DISPLAY,
                  OFF_DISPLAY_MESSAGE
               )
               VALUES (?, ?, 0, NULL)
               ON CONFLICT(SPECIES, EXHIBIT) DO UPDATE SET
                  IS_OFF_DISPLAY = 0,
                  OFF_DISPLAY_MESSAGE = NULL;
         """,
         (
            species,
            exhibit,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
