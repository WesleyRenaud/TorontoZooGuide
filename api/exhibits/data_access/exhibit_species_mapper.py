from __future__ import annotations

from ..domain.exhibit_species import ExhibitSpecies
from ...types import Types


class ExhibitSpeciesMapper():
   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ ExhibitSpecies ]:
      return [
         cls.map_exhibit( exhibit, rows )
         for exhibit in cls.exhibit_names( rows )
      ]


   @classmethod
   def exhibit_names( cls, rows: list[ Types.Row ] ) -> list[ str ]:
      names: list[ str ] = []

      for row in rows:
         name = row[ 'EXHIBIT' ]

         if name not in names:
            names.append( name )

      return names


   @classmethod
   def map_exhibit( cls, exhibit: str, rows: list[ Types.Row ] ) -> ExhibitSpecies:
      return ExhibitSpecies(
         exhibit=exhibit,
         species=cls.species_names( exhibit, rows ),
      )


   @classmethod
   def species_names( cls, exhibit: str, rows: list[ Types.Row ] ) -> list[ str ]:
      names: list[ str ] = []

      for row in rows:
         if row[ 'EXHIBIT' ] != exhibit:
            continue

         species = row[ 'SPECIES' ]

         if species not in names:
            names.append( species )

      return names
