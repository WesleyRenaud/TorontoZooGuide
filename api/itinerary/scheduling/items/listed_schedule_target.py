from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class ListedScheduleTarget:
   default_duration_seconds: int | None
