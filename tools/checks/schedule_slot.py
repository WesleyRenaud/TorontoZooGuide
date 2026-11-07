from __future__ import annotations

from dataclasses import dataclass
from datetime import time


@dataclass( frozen=True )
class ScheduleSlot:
   weekday: int
   time: time
