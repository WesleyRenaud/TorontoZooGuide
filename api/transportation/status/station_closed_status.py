from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey


@dataclass( frozen=True )
class TransportationStationClosedStatus:
   transportation_station: str
   start_date: str
   end_date: DateKey | None
   message: str
