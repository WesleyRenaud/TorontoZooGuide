from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class AttractionHours:
   weekday_opens: str | None = None
   weekday_closes: str | None = None
   weekend_opens: str | None = None
   weekend_closes: str | None = None
