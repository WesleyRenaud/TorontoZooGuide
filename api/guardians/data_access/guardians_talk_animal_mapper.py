from __future__ import annotations

from ...animals.search.species_exhibit_key import SpeciesExhibitKey
from ...types import Row


def map_guardians_talk_linked_animal( row: Row ) -> SpeciesExhibitKey:
   return SpeciesExhibitKey.from_values(
      row[ 'SPECIES' ],
      row[ 'EXHIBIT' ] )


def map_guardians_talk_linked_animals(
      rows: list[ Row ] ) -> list[ SpeciesExhibitKey ]:
   return [
      map_guardians_talk_linked_animal( row )
      for row in rows
   ]
