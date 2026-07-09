from __future__ import annotations

from ...types import Connection
from .wild_encounter_meeting_spot_loop_pin_mapper import index_wild_encounter_meeting_spot_loop_pin_records_by_name
from .wild_encounter_meeting_spot_loop_pin_mapper import map_wild_encounter_meeting_spot_loop_pin_records
from .wild_encounter_meeting_spot_loop_pin_record import WildEncounterMeetingSpotLoopPinRecord


def fetch_wild_encounter_meeting_spot_loop_pins_by_name(
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

      return index_wild_encounter_meeting_spot_loop_pin_records_by_name(
         map_wild_encounter_meeting_spot_loop_pin_records( data.fetchall() ) )

   finally:
      cur.close()
