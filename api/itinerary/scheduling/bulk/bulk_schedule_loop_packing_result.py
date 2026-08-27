from __future__ import annotations

from dataclasses import dataclass

from .attraction_animal_coverer import CoveredAnimalAttraction
from .guardians_talk_animal_coverer import CoveredAnimalTalk
from .loop_schedule_stop import LoopScheduleStop
from .loop_schedule_unit import LoopScheduleUnit
from ...routing.itinerary_schedule_window import ItineraryScheduleWindow
from ....walk_graph.domain.viewing_spot_name_key import ViewingSpotNameKey


@dataclass( frozen=True )
class BulkScheduleLoopPackingResult:
   remaining_stops: list[ LoopScheduleStop ]
   covered_by_talk: dict[ ViewingSpotNameKey, CoveredAnimalTalk ]
   covered_by_attraction: dict[ ViewingSpotNameKey, CoveredAnimalAttraction ]
   schedule_windows: list[ ItineraryScheduleWindow ]
   loop_units: list[ LoopScheduleUnit ]
