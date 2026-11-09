from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from tools.checks.schedule_slot import ScheduleSlot


@dataclass( frozen=True )
class GuardiansTalkWindowCorrection:
   name: str
   location: str
   start: date
   end: date
   slots: set[ ScheduleSlot ]
