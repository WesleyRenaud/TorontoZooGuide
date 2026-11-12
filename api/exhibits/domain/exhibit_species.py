from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class ExhibitSpecies():
   exhibit: str
   species: list[ str ]
