from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class EnclosureOffDisplayMonth:
   species: str
   exhibit: str
   until_month: int | None
