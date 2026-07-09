from __future__ import annotations

from collections.abc import Iterable

from ...types import Row
from .wild_encounter_meeting_spot_loop_pin_record import WildEncounterMeetingSpotLoopPinRecord


def map_wild_encounter_meeting_spot_loop_pin_record(
      row: Row ) -> WildEncounterMeetingSpotLoopPinRecord:
   return WildEncounterMeetingSpotLoopPinRecord(
      name=row[ 'NAME' ],
      loop_id=row[ 'LOOP_ID' ],
      loop_viewing_spot_index=row[ 'LOOP_VIEWING_SPOT_INDEX' ] )


def map_wild_encounter_meeting_spot_loop_pin_records(
      rows: Iterable[ Row ],
   ) -> list[ WildEncounterMeetingSpotLoopPinRecord ]:
   return [
      map_wild_encounter_meeting_spot_loop_pin_record( row )
      for row in rows
   ]


def index_wild_encounter_meeting_spot_loop_pin_records_by_name(
      records: Iterable[ WildEncounterMeetingSpotLoopPinRecord ],
   ) -> dict[ str, WildEncounterMeetingSpotLoopPinRecord ]:
   pins_by_name: dict[ str, WildEncounterMeetingSpotLoopPinRecord ] = {}

   for record in records:
      pins_by_name[ record.name ] = record

   return pins_by_name
