from __future__ import annotations

from ...types import Types
from .wild_encounter_meeting_spot_loop_pin_record import WildEncounterMeetingSpotLoopPinRecord


class WildEncounterMeetingSpotLoopPinMapper():
   @classmethod
   def map_record(
         cls,
         row: Types.Row ) -> WildEncounterMeetingSpotLoopPinRecord:
      return WildEncounterMeetingSpotLoopPinRecord(
         name=row[ 'NAME' ],
         loop_id=row[ 'LOOP_ID' ],
         loop_viewing_spot_index=row[ 'LOOP_VIEWING_SPOT_INDEX' ] )


   @classmethod
   def map_records(
         cls,
         rows: list[ Types.Row ],
      ) -> list[ WildEncounterMeetingSpotLoopPinRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]


   @classmethod
   def index_by_name(
         cls,
         records: list[ WildEncounterMeetingSpotLoopPinRecord ],
      ) -> dict[ str, WildEncounterMeetingSpotLoopPinRecord ]:
      pins_by_name: dict[ str, WildEncounterMeetingSpotLoopPinRecord ] = {}

      for record in records:
         pins_by_name[ record.name ] = record

      return pins_by_name
