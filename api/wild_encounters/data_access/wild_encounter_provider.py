from __future__ import annotations

from ...types import Connection
from .wild_encounter_mapper import WildEncounterMapper
from .wild_encounter_record import WildEncounterRecord


class WildEncounterProvider():
   @classmethod
   def fetch_wild_encounter_names( cls, conn: Connection ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     w.NAME
                  FROM WildEncounter w;
            """ )

         return [
            row[ 'NAME' ]
            for row in data.fetchall()
         ]

      finally:
         cur.close()


   @classmethod
   def fetch_wild_encounter_records( cls, conn: Connection ) -> list[ WildEncounterRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     w.NAME,
                     w.MEETING_SPOT,
                     w.LINK,
                     w.MAXIMUM_DURATION,
                     m.X_COORD,
                     m.Y_COORD,
                     m.REGION
                  FROM WildEncounter w
                  JOIN WildEncounterMeetingSpot m
                     ON w.MEETING_SPOT = m.NAME;
            """ )

         return WildEncounterMapper.map_records( data.fetchall() )

      finally:
         cur.close()
