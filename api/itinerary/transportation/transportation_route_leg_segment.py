from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class TransportationRouteLegSegment:
   from_station: str
   to_station: str
   duration_minutes: int
