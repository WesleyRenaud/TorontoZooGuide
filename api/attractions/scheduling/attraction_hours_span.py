from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass( frozen=True )
class AttractionHoursSpan:
   start: date
   end: date | None
