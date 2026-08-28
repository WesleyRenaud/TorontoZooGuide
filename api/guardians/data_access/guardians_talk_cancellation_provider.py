from __future__ import annotations

from ..cancellations.guardians_talk_cancellation_input import GuardiansTalkCancellationInput
from .guardians_talk_cancellation_mapper import GuardiansTalkCancellationMapper
from .guardians_talk_cancellation_record import GuardiansTalkCancellationRecord
from ...types import Types


class GuardiansTalkCancellationProvider():
   @classmethod
   def fetch_cancellation_records(
         cls,
         conn: Types.Connection,
         talk_name: str,
         location: str ) -> list[ GuardiansTalkCancellationRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     CANCELLATION_DATE,
                     TALK_TIME
                  FROM GuardiansTalkCancellation
                  WHERE TALK_NAME = ?
                  AND LOCATION = ?;
            """,
            (
               talk_name,
               location,
            ) )

         return GuardiansTalkCancellationMapper.map_records( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def fetch_occurrence_is_cancelled(
         cls,
         conn: Types.Connection,
         talk_name: str,
         location: str,
         cancellation_date: Types.DateKey,
         talk_time: str ) -> bool:
      cur = conn.cursor()

      try:
         cancellation_data = cur.execute(
            """   SELECT 1
                     FROM GuardiansTalkCancellation
                     WHERE TALK_NAME = ?
                     AND LOCATION = ?
                     AND CANCELLATION_DATE = ?
                     AND TALK_TIME = ?;
               """,
            (
               talk_name,
               location,
               cancellation_date,
               talk_time,
            ) )

         return cancellation_data.fetchone() != None

      finally:
         cur.close()


   @classmethod
   def save_cancellation(
         cls,
         conn: Types.Connection,
         cancellation: GuardiansTalkCancellationInput ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO GuardiansTalkCancellation (
                     TALK_NAME,
                     LOCATION,
                     CANCELLATION_DATE,
                     TALK_TIME
                  )
                  VALUES (?, ?, ?, ?)
                  ON CONFLICT(TALK_NAME, LOCATION, CANCELLATION_DATE, TALK_TIME)
                  DO NOTHING;
            """,
            (
               cancellation.talk_name,
               cancellation.location,
               cancellation.cancellation_date,
               cancellation.talk_time,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()
