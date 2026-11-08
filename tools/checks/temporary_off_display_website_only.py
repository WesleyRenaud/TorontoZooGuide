from __future__ import annotations

from dataclasses import dataclass

from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit


@dataclass( frozen=True )
class TemporaryOffDisplayWebsiteOnly:
   enclosures: list[ AnimalSpeciesExhibit ]
   unmatched: list[ str ]
