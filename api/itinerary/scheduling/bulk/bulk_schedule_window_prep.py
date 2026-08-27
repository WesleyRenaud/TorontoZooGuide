from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from .bulk_schedule_start_state import BulkScheduleStartState
from ..core.time_block import TimeBlock
from ...data_access.saved_itinerary import SavedItinerary
from ....models import Itinerary
from ...routing.loop_schedule_pin import LoopSchedulePin
from ...routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from ....shared.operating_hours import OperatingHours
from ....walk_graph.domain.walk_graph import WalkGraph


@dataclass( frozen=True )
class BulkScheduleWindowPrep:
   saved_itinerary: SavedItinerary
   previous_itinerary: Itinerary
   itinerary_context: dict[ str, Any ]
   anchor_seconds: int
   day_end_seconds: int
   blockers: list[ TimeBlock ]
   walk_graph: WalkGraph
   start_state: BulkScheduleStartState
   schedule_windows: list[ ItineraryScheduleWindow ]
   loop_pins: list[ LoopSchedulePin ]
   visit_date: date | None
   zoo_operating_hours: OperatingHours | None
