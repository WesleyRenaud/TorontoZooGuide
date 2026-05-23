from __future__ import annotations

from typing import TYPE_CHECKING

from ...types import Connection

if TYPE_CHECKING:
   from ..logic.guardians_talk_cancellation_input import GuardiansTalkCancellationInput


def save_guardians_talk_cancellation(
      conn: Connection,
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
