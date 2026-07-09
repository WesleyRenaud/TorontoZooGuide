from __future__ import annotations

from dataclasses import dataclass

from .itinerary_stop import ItineraryStop


@dataclass( frozen=True )
class LoopSchedulePin:
   loop_id: str
   viewing_spot_index: int
   stop: ItineraryStop
   start_seconds: int
   end_seconds: int
