from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class AnimalSpeciesExhibit:
   species: str
   exhibit: str
   image: str = ''
