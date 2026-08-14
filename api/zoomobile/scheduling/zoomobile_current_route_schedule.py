from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey


@dataclass( frozen=True )
class ZoomobileCurrentRouteSchedule:
   route: str
   start_date: str
   end_date: DateKey | None
