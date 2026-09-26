from __future__ import annotations

from dataclasses import dataclass

from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ...types import Types


@dataclass( frozen=True )
class VisitWindowOverflowResolution:
   kept_items: list[ ItinerarySaveIssueItem ]
   dropped_items: list[ ItinerarySaveIssueItem ]
   arrival_time: Types.ScheduleTimeKey
   departure_time: Types.ScheduleTimeKey
