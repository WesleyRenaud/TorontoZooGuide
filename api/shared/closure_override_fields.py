from __future__ import annotations

from dataclasses import dataclass

from ..types import Types


@dataclass( frozen=True )
class ClosureOverrideFields:
   start_date: Types.DateKey
   end_date: Types.DateKey | None
   is_closed: bool
   message: str | None
