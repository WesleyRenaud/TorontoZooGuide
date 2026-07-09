from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class WildEncounterMeetingSpotLoopPinRecord:
   name: str
   loop_id: str
   loop_viewing_spot_index: int
