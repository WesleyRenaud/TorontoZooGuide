from __future__ import annotations

from ...types import Connection, DateInput


class AnimalVisibilityScheduleProvider():
   @classmethod
   def save_animal_limited_viewing_schedule(
         cls,
         conn: Connection,
         species: str,
         exhibit: str,
         start_date: DateInput,
         end_date: DateInput,
         daily_start_time: str,
         daily_end_time: str,
         message: str ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO AnimalVisibilitySchedule (
                     SPECIES,
                     EXHIBIT,
                     SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE,
                     DAILY_START_TIME,
                     DAILY_END_TIME,
                     VIEWING_MESSAGE
                  )
                  VALUES (?, ?, ?, ?, ?, ?, ?)
                  ON CONFLICT(SPECIES, EXHIBIT) DO UPDATE SET
                     SCHEDULE_START_DATE = excluded.SCHEDULE_START_DATE,
                     SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                     DAILY_START_TIME = excluded.DAILY_START_TIME,
                     DAILY_END_TIME = excluded.DAILY_END_TIME,
                     VIEWING_MESSAGE = excluded.VIEWING_MESSAGE;
            """,
            (
               species,
               exhibit,
               start_date,
               end_date,
               daily_start_time,
               daily_end_time,
               message,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def delete_animal_visibility_schedule(
         cls,
         conn: Connection,
         species: str,
         exhibit: str ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """ DELETE FROM AnimalVisibilitySchedule
               WHERE SPECIES = ?
                  AND EXHIBIT = ?;
            """,
            (
               species,
               exhibit,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()
