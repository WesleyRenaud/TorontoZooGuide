from __future__ import annotations

from ...types import Types


class AnimalViewingAlertProvider():
   @classmethod
   def _clear_animal_viewing_alert(
         cls,
         cur: Types.Cursor,
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


   @classmethod
   def _insert_animal_viewing_alert(
         cls,
         cur: Types.Cursor,
         species: str,
         exhibit: str,
         alert_start_date: Types.DateInput,
         alert_end_date: Types.DateInput,
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


   @classmethod
   def save_animal_viewing_alert(
         cls,
         conn: Types.Connection,
         species: str,
         exhibit: str,
         alert_start_date: Types.DateInput,
         alert_end_date: Types.DateInput,
         message: str ) -> bool:
      cur = conn.cursor()

      try:
         cls._clear_animal_viewing_alert(
            cur,
            species=species,
            exhibit=exhibit )
         cls._insert_animal_viewing_alert(
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


   @classmethod
   def delete_animal_viewing_alert(
         cls,
         conn: Types.Connection,
         species: str,
         exhibit: str ) -> bool:
      cur = conn.cursor()

      try:
         cls._clear_animal_viewing_alert(
            cur,
            species=species,
            exhibit=exhibit )
         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()
