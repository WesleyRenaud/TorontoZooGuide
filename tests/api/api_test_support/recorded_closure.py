from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class RecordedClosure:
   name: str
   start_date: str
   end_date: str
   message: str
