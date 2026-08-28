from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class TransportationStationStatusRecord:
   station: str
   closed_start: Types.DateKey
   closed_end: Types.DateKey | None
   is_closed: bool
   closed_message: str | None
