from __future__ import annotations

from dataclasses import dataclass

from ..types import DateKey


@dataclass( frozen=True )
class ClosureOverrideFields:
   start_date: DateKey
   end_date: DateKey | None
   is_closed: bool
   message: str | None
