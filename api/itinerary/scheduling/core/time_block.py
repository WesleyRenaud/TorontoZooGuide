from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class TimeBlock:
   start_seconds: int
   end_seconds: int
