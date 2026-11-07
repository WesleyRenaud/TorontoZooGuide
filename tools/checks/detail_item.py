from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DetailItem:
   title: str
   details: list[ str ]
