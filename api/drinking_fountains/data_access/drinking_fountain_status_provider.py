from __future__ import annotations

from datetime import date

from .drinking_fountain_status_mapper import DrinkingFountainStatusMapper
from .drinking_fountain_status_record import DrinkingFountainStatusRecord
from ...types import Types


class DrinkingFountainStatusProvider():
   @classmethod
   def fetch_drinking_fountain_status_record(
         cls,
         conn: Types.Connection ) -> DrinkingFountainStatusRecord | None:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     IS_CLOSED,
                     START_DATE,
                     END_DATE,
                     CLOSED_MESSAGE
                  FROM DrinkingFountainStatus
                  LIMIT 1;
            """ )

         row = data.fetchone()

         if row is None:
            return None

         return DrinkingFountainStatusMapper.map_record( row )

      finally:
         cur.close()


   @classmethod
   def fetch_current_drinking_fountain_status_record(
         cls,
         conn: Types.Connection ) -> DrinkingFountainStatusRecord:
      cur = conn.cursor()

      try:
         row = cur.execute(
            """   SELECT
                     COALESCE( status.IS_CLOSED, 0 ) AS IS_CLOSED,
                     status.START_DATE AS START_DATE,
                     status.END_DATE AS END_DATE,
                     status.CLOSED_MESSAGE AS CLOSED_MESSAGE
                  FROM ( SELECT 1 ) AS anchor
                  LEFT JOIN DrinkingFountainStatus AS status
                  LIMIT 1;
            """
         ).fetchone()

         return DrinkingFountainStatusMapper.map_record( row )

      finally:
         cur.close()


   @classmethod
   def fetch_drinking_fountain_seasonal_likelihood(
         cls,
         conn: Types.Connection,
         target_date: date ) -> float:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     LIKELIHOOD
                  FROM DrinkingFountainDaySeasonalAvailabilityMultiplier
                  WHERE MONTH = ?
                     AND DAY = ?;
            """,
            (
               target_date.month,
               target_date.day
            ) )

         row = data.fetchone()

         return row[ 'LIKELIHOOD' ] if row else 1.0

      finally:
         cur.close()


   @classmethod
   def save_drinking_fountain_status(
         cls,
         conn: Types.Connection,
         *,
         is_closed: bool,
         start_date: Types.DateKey | None,
         end_date: Types.DateKey | None,
         message: str | None ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute( 'DELETE FROM DrinkingFountainStatus;' )

         cur.execute(
            """   INSERT INTO DrinkingFountainStatus (
                     IS_CLOSED,
                     START_DATE,
                     END_DATE,
                     CLOSED_MESSAGE
                  )
                  VALUES (?, ?, ?, ?);
            """,
            (
               is_closed,
               start_date,
               end_date,
               message,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def delete_drinking_fountain_status( cls, conn: Types.Connection ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute( 'DELETE FROM DrinkingFountainStatus;' )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()
