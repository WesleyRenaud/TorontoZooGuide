from __future__ import annotations

from typing import TYPE_CHECKING

from ...types import Connection

if TYPE_CHECKING:
   from ..logic.wild_encounter_cancellation_input import WildEncounterCancellationInput


def save_wild_encounter_cancellation(
      conn: Connection,
      cancellation: WildEncounterCancellationInput ) -> bool:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO WildEncounterCancellation (
                  WILD_ENCOUNTER,
                  CANCELLATION_DATE,
                  ENCOUNTER_TIME
               )
               VALUES (?, ?, ?)
               ON CONFLICT(WILD_ENCOUNTER, CANCELLATION_DATE, ENCOUNTER_TIME)
               DO NOTHING;
         """,
         (
            cancellation.wild_encounter,
            cancellation.cancellation_date,
            cancellation.encounter_time,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
