from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass( frozen=True )
class AttractionHoursCoverage:
   stops_fitting_on: date | None
   both_day_kinds: bool
