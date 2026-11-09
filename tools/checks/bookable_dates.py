from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass( frozen=True )
class BookableDates:
   dates: list[ date ]
   failure: str | None
