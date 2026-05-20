def save_animal_viewing_alert(
      conn,
      species,
      exhibit,
      alert_start_date,
      alert_end_date,
      message ):
   cur = conn.cursor()

   try:
      clear_animal_viewing_alert_with_cursor(
         cur,
         species=species,
         exhibit=exhibit )
      insert_animal_viewing_alert_with_cursor(
         cur,
         species=species,
         exhibit=exhibit,
         alert_start_date=alert_start_date,
         alert_end_date=alert_end_date,
         message=message )
      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def clear_animal_viewing_alert_with_cursor( cur, species, exhibit ):
   cur.execute(
      """ DELETE FROM AnimalViewingAlert
          WHERE SPECIES = ?
          AND EXHIBIT = ?;
      """,
      (
         species,
         exhibit,
      ) )


def delete_animal_viewing_alert( conn, species, exhibit ):
   cur = conn.cursor()

   try:
      clear_animal_viewing_alert_with_cursor(
         cur,
         species=species,
         exhibit=exhibit )
      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def insert_animal_viewing_alert_with_cursor(
      cur,
      species,
      exhibit,
      alert_start_date,
      alert_end_date,
      message ):
   cur.execute(
      """   INSERT INTO AnimalViewingAlert (
               SPECIES,
               EXHIBIT,
               ALERT_MESSAGE,
               ALERT_START_DATE,
               ALERT_END_DATE
            )
            VALUES (?, ?, ?, ?, ?)
      """,
      (
         species,
         exhibit,
         message,
         alert_start_date,
         alert_end_date,
      ) )
