from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from ...data_access.saved_itinerary import SavedItinerary
from ....shared.operating_hours import OperatingHours


@dataclass( frozen=True )
class PreparedScheduleWindow:
   saved_itinerary: SavedItinerary
   window: tuple[ int, int ]
   visit_date: date
   zoo_operating_hours: OperatingHours | None = None
