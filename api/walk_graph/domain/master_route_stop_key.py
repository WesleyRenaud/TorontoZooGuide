from __future__ import annotations

from ...shared.enums import ScheduleItemKind


AnimalMasterRouteStopKey = tuple[ ScheduleItemKind, str, str, str | None ]
AttractionMasterRouteStopKey = tuple[ ScheduleItemKind, str ]
MasterRouteStopKey = AnimalMasterRouteStopKey | AttractionMasterRouteStopKey
