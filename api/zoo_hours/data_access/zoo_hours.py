from __future__ import annotations

from ...types import Connection, DateKey
from .zoo_hours_mapper import map_zoo_hours_record
from .zoo_hours_record import ZooHoursRecord


def fetch_zoo_hours_record( conn: Connection, operating_date: DateKey ) -> ZooHoursRecord | None:
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

      return map_zoo_hours_record( row )

   finally:
      cur.close()


def fetch_zoo_hours_records_between(
      conn: Connection,
      start_date: DateKey,
      end_date: DateKey | None = None ) -> list[ ZooHoursRecord ]:
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

      return [ map_zoo_hours_record( row ) for row in rows ]

   finally:
      cur.close()
