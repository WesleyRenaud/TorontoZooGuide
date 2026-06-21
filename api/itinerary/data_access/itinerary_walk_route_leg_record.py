from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import ScheduleItemKind


@dataclass( frozen=True )
class ItineraryWalkRouteLegRecord:
   leg_sequence: int
   from_item_key: str
   to_item_key: str
   from_schedule_item_kind: ScheduleItemKind
   to_schedule_item_kind: ScheduleItemKind
   from_point_sequence: int
   to_point_sequence: int
