from __future__ import annotations

from ...types import Types
from .zoo_hours_mapper import ZooHoursMapper
from .zoo_hours_record import ZooHoursRecord


class ZooHoursProvider():
   @classmethod
   def fetch_zoo_hours_record(
         cls,
         conn: Types.Connection,
         operating_date: Types.DateKey ) -> ZooHoursRecord | None:
      cur = conn.cursor()

      try:
         row = cur.execute(
            """   SELECT
                     OPERATING_DATE,
                     EARLY_ADMISSION_TIME,
                     OPEN_TIME,
                     LAST_ADMISSION_TIME,
                     CLOSE_TIME
                  FROM ZooHours
                  WHERE OPERATING_DATE = ?;
            """,
            ( operating_date, ) ).fetchone()

         if row == None:
            return None

         return ZooHoursMapper.map_record( row )

      finally:
         cur.close()


   @classmethod
   def fetch_zoo_hours_records_between(
         cls,
         conn: Types.Connection,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None = None ) -> list[ ZooHoursRecord ]:
      cur = conn.cursor()

      try:
         if end_date is None:
            rows = cur.execute(
               """   SELECT
                        OPERATING_DATE,
                        EARLY_ADMISSION_TIME,
                        OPEN_TIME,
                        LAST_ADMISSION_TIME,
                        CLOSE_TIME
                     FROM ZooHours
                     WHERE OPERATING_DATE >= ?
                     ORDER BY OPERATING_DATE;
               """,
               ( start_date, ) ).fetchall()
         else:
            rows = cur.execute(
               """   SELECT
                        OPERATING_DATE,
                        EARLY_ADMISSION_TIME,
                        OPEN_TIME,
                        LAST_ADMISSION_TIME,
                        CLOSE_TIME
                     FROM ZooHours
                     WHERE OPERATING_DATE >= ?
                        AND OPERATING_DATE <= ?
                     ORDER BY OPERATING_DATE;
               """,
               ( start_date, end_date ) ).fetchall()

         return ZooHoursMapper.map_records( rows )

      finally:
         cur.close()


   @classmethod
   def save_zoo_hours( cls, conn: Types.Connection, record: ZooHoursRecord ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO ZooHours (
                     OPERATING_DATE,
                     EARLY_ADMISSION_TIME,
                     OPEN_TIME,
                     LAST_ADMISSION_TIME,
                     CLOSE_TIME
                  )
                  VALUES ( ?, ?, ?, ?, ? )
                  ON CONFLICT( OPERATING_DATE ) DO UPDATE SET
                     EARLY_ADMISSION_TIME = excluded.EARLY_ADMISSION_TIME,
                     OPEN_TIME = excluded.OPEN_TIME,
                     LAST_ADMISSION_TIME = excluded.LAST_ADMISSION_TIME,
                     CLOSE_TIME = excluded.CLOSE_TIME;
            """,
            (
               record.operating_date,
               record.early_admission_time,
               record.open_time,
               record.last_admission_time,
               record.close_time,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def delete_zoo_hours( cls, conn: Types.Connection, operating_date: Types.DateKey ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   DELETE FROM ZooHours
                  WHERE OPERATING_DATE = ?;
            """,
            ( operating_date, ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()
