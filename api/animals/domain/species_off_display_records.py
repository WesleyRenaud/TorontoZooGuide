from __future__ import annotations

from dataclasses import dataclass

from ..data_access.animal_off_display_record import AnimalOffDisplayRecord


@dataclass( frozen=True )
class SpeciesOffDisplayRecords:
   species: str
   records: list[ AnimalOffDisplayRecord ]


   @classmethod
   def groups(
         cls,
         species: list[ str ],
         records: list[ AnimalOffDisplayRecord ] ) -> list[ SpeciesOffDisplayRecords ]:
      return [
         cls(
            species=name,
            records=[
               record
               for record in records
               if record.species == name
            ],
         )
         for name in species
      ]
