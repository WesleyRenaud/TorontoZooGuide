from __future__ import annotations

from dataclasses import dataclass

from .count import Count
from .section import Section


@dataclass
class Report:
   sections: list[ Section ]
   counts: list[ Count ]
   error_count: int | None
