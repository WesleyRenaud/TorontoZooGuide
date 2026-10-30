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
         location: str,
         *,
         enclosure_name: str ) -> list[ GuardiansTalkCancellationRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     CANCELLATION_DATE,
                     TALK_TIME
                  FROM GuardiansTalkCancellation
                  WHERE TALK_NAME = ?
                  AND LOCATION = ?
                  AND ENCLOSURE_NAME IS ?;
            """,
            (
               talk_name,
               location,
               enclosure_name,
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
         talk_time: str,
         *,
         enclosure_name: str ) -> bool:
      cur = conn.cursor()

      try:
         cancellation_data = cur.execute(
            """   SELECT 1
                     FROM GuardiansTalkCancellation
                     WHERE TALK_NAME = ?
                     AND LOCATION = ?
                     AND ENCLOSURE_NAME IS ?
                     AND CANCELLATION_DATE = ?
                     AND TALK_TIME = ?;
               """,
            (
               talk_name,
               location,
               enclosure_name,
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
                     ENCLOSURE_NAME,
                     CANCELLATION_DATE,
                     TALK_TIME
                  )
                  VALUES (?, ?, ?, ?, ?)
                  ON CONFLICT(TALK_NAME, LOCATION, ENCLOSURE_NAME, CANCELLATION_DATE, TALK_TIME)
                  DO NOTHING;
            """,
            (
               cancellation.talk_name,
               cancellation.location,
               cancellation.enclosure_name,
               cancellation.cancellation_date,
               cancellation.talk_time,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()
