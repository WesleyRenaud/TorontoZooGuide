from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AnimalListing:
   exhibit: str
   species: list[ str ]
