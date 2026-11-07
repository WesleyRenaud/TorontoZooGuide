from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .programme_talk import ProgrammeTalk


@dataclass( frozen=True )
class ProgrammeDay:
   scheduled_date: date
   talks: list[ ProgrammeTalk ]
