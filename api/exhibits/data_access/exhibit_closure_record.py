from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey


@dataclass( frozen=True )
class ExhibitClosureRecord:
   exhibit: str
   closed_start: DateKey
   closed_end: DateKey | None
