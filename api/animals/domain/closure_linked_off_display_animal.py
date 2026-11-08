from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass( frozen=True )
class ClosureLinkedOffDisplayAnimal:
   species: str
   exhibit: str
   end: date | None
   closure_update_title: str
   closure_update_start: date
