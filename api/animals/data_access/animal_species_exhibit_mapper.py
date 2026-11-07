from __future__ import annotations

from ..domain.animal_species_exhibit import AnimalSpeciesExhibit
from ...types import Types


class AnimalSpeciesExhibitMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> AnimalSpeciesExhibit:
      return AnimalSpeciesExhibit(
         species=row[ 'SPECIES' ],
         exhibit=row[ 'EXHIBIT' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ AnimalSpeciesExhibit ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
