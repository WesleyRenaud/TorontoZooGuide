from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey


@dataclass( frozen=True )
class ZoomobileStationStatusRecord:
   station: str
   closed_start: DateKey
   closed_end: DateKey | None
   is_closed: bool
   closed_message: str | None
