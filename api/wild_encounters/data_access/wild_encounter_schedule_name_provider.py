from __future__ import annotations

from ...shared.enums.position import Position
from ...types import Types


class WildEncounterScheduleNameProvider():
   @classmethod
   def fetch_scheduled_wild_encounter_names(
         cls,
         conn: Types.Connection,
         today: Types.DateKey ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     WILD_ENCOUNTER
                  FROM WildEncounterSchedule
                  WHERE SCHEDULE_END_DATE IS NULL
                     OR SCHEDULE_END_DATE > ?
                  ORDER BY WILD_ENCOUNTER;
            """,
            ( today, ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()
