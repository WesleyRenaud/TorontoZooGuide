from __future__ import annotations

from typing import TypeAlias

from ...shared.enums import ScheduleItemKind


class AttractionMasterRouteStopKey():
   Key: TypeAlias = tuple[ ScheduleItemKind, str ]
