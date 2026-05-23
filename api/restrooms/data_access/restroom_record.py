from __future__ import annotations

from dataclasses import dataclass

from ...types import Coordinate, DateKey


@dataclass( frozen=True )
class RestroomRecord:
   title: str
   x_coord: Coordinate
   y_coord: Coordinate
   is_closed: bool | None
   closed_message: str | None
   closed_start: DateKey | None
   closed_end: DateKey | None
   alert_message: str | None
   alert_start_date: DateKey | None
   alert_end_date: DateKey | None
