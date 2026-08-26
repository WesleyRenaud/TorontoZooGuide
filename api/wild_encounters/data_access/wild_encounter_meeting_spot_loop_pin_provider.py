from __future__ import annotations

from ...types import Connection
from .wild_encounter_meeting_spot_loop_pin_mapper import WildEncounterMeetingSpotLoopPinMapper
from .wild_encounter_meeting_spot_loop_pin_record import WildEncounterMeetingSpotLoopPinRecord


class WildEncounterMeetingSpotLoopPinProvider():
   @classmethod
   def fetch_meeting_spot_loop_pins_by_name(
         cls,
         conn: Connection,
      ) -> dict[ str, WildEncounterMeetingSpotLoopPinRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     NAME,
                     LOOP_ID,
                     LOOP_VIEWING_SPOT_INDEX
                  FROM WildEncounterMeetingSpot
                  WHERE LOOP_ID IS NOT NULL
                    AND LOOP_VIEWING_SPOT_INDEX IS NOT NULL;
            """ )

         return WildEncounterMeetingSpotLoopPinMapper.index_by_name(
            WildEncounterMeetingSpotLoopPinMapper.map_records( data.fetchall() ) )

      finally:
         cur.close()
