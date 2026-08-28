from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class RestroomRecord:
   title: str
   x_coord: Types.Coordinate
   y_coord: Types.Coordinate
   is_closed: bool | None
   closed_message: str | None
   closed_start: Types.DateKey | None
   closed_end: Types.DateKey | None
   alert_message: str | None
   alert_start_date: Types.DateKey | None
   alert_end_date: Types.DateKey | None
