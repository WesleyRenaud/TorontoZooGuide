from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass( frozen=True )
class ProgrammeTalk:
   scheduled_date: date
   talk_time: str
   name: str
   location: str
