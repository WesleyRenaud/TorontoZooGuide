from __future__ import annotations

from ...shared.enums.position import Position
from ...types import Types


class GuardiansTalkScheduleNameProvider():
   @classmethod
   def fetch_scheduled_talk_names(
         cls,
         conn: Types.Connection,
         today: Types.DateKey,
         location: str ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     TALK_NAME
                  FROM GuardiansTalkSchedule
                  WHERE LOCATION = ?
                     AND (
                        SCHEDULE_END_DATE IS NULL
                        OR SCHEDULE_END_DATE > ?
                     )
                  ORDER BY TALK_NAME;
            """,
            ( location, today ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()


   @classmethod
   def fetch_scheduled_talk_locations(
         cls,
         conn: Types.Connection,
         today: Types.DateKey ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     LOCATION
                  FROM GuardiansTalkSchedule
                  WHERE SCHEDULE_END_DATE IS NULL
                     OR SCHEDULE_END_DATE > ?
                  ORDER BY LOCATION;
            """,
            ( today, ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()
