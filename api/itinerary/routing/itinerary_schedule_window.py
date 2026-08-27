from __future__ import annotations

from dataclasses import dataclass, field

from .attraction_hours_soft_pin import AttractionHoursSoftPin
from .itinerary_stop import ItineraryStop
from .loop_schedule_pin import LoopSchedulePin


@dataclass( frozen=True )
class ItineraryScheduleWindow:
   start_seconds: int
   end_seconds: int
   anchor_stop: ItineraryStop | None = None
   loop_pins: list[ LoopSchedulePin ] = field( default_factory=list )
   attraction_hours_soft_pins: list[ AttractionHoursSoftPin ] = field(
      default_factory=list )
   opens_after_fixed_time_stop: bool = False
   start_walk_node_id: str | None = None
