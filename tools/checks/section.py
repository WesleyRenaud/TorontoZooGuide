from __future__ import annotations

from dataclasses import dataclass

from .category import Category


@dataclass
class Section:
   kind: str
   day: str
   note: str
   categories: list[ Category ]
