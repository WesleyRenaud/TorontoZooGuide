from __future__ import annotations

from dataclasses import dataclass

from .detail_item import DetailItem


@dataclass
class Category:
   title: str
   count: int
   items: list[ DetailItem ]
