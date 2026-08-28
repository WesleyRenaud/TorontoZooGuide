from __future__ import annotations

from ..cancellations.wild_encounter_cancellation_input import WildEncounterCancellationInput
from ...types import Types
from .wild_encounter_cancellation_mapper import WildEncounterCancellationMapper
from .wild_encounter_cancellation_record import WildEncounterCancellationRecord


class WildEncounterCancellationProvider():
   @classmethod
   def fetch_cancellation_records(
         cls,
         conn: Types.Connection,
         wild_encounter: str ) -> list[ WildEncounterCancellationRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     CANCELLATION_DATE,
                     ENCOUNTER_TIME
                  FROM WildEncounterCancellation
                  WHERE WILD_ENCOUNTER = ?;
            """,
            ( wild_encounter, ) )

         return WildEncounterCancellationMapper.map_records( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def save_cancellation(
         cls,
         conn: Types.Connection,
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
