from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class AttractionHoursSoftPin:
   loop_id: str
   viewing_spot_index: int
   attraction_name: str
   open_seconds: int
   close_seconds: int
