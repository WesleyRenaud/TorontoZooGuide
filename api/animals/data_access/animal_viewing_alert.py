from __future__ import annotations

from ...types import Connection, Cursor, DateInput


def save_animal_viewing_alert(
      conn: Connection,
      species: str,
      exhibit: str,
      alert_start_date: DateInput,
      alert_end_date: DateInput,
      message: str ) -> bool:
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


def clear_animal_viewing_alert_with_cursor(
      cur: Cursor,
      species: str,
      exhibit: str ) -> None:
   cur.execute(
      """ DELETE FROM AnimalViewingAlert
          WHERE SPECIES = ?
          AND EXHIBIT = ?;
      """,
      (
         species,
         exhibit,
      ) )


def delete_animal_viewing_alert( conn: Connection, species: str, exhibit: str ) -> bool:
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
      cur: Cursor,
      species: str,
      exhibit: str,
      alert_start_date: DateInput,
      alert_end_date: DateInput,
      message: str ) -> None:
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
