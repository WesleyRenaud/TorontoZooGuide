from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class ItineraryStatusRecord:
   status: str
   is_suppressable: bool
   is_suppressed: bool
