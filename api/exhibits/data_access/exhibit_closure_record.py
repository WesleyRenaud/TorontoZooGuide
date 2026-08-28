from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class ExhibitClosureRecord:
   exhibit: str
   closed_start: Types.DateKey
   closed_end: Types.DateKey | None
