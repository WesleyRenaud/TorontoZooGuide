from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from tools.checks.schedule_slot import ScheduleSlot


@dataclass( frozen=True )
class EncounterScheduleCorrection:
   name: str
   start: date
   end: date
   slots: set[ ScheduleSlot ]
