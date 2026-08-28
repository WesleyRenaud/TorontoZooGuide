from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class TransportationCurrentRouteSchedule:
   route: str
   start_date: str
   end_date: Types.DateKey | None
