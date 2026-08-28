from __future__ import annotations

from typing import TypeAlias

from ...shared.enums import ScheduleItemKind


class AnimalMasterRouteStopKey():
   Key: TypeAlias = tuple[ ScheduleItemKind, str, str, str | None ]
