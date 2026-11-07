from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RegionColor:
   region: str
   background: str
   foreground: str
