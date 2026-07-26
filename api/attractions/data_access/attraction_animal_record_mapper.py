from __future__ import annotations

from .attraction_animal_record import AttractionAnimalRecord
from ...types import Row


def map_attraction_animal_record( row: Row ) -> AttractionAnimalRecord:
   return AttractionAnimalRecord(
      attraction=row[ 'ATTRACTION' ],
      species=row[ 'SPECIES' ],
      exhibit=row[ 'EXHIBIT' ],
      enclosure_name=row[ 'ENCLOSURE_NAME' ] )


def map_attraction_animal_records(
      rows: list[ Row ] ) -> list[ AttractionAnimalRecord ]:
   return [
      map_attraction_animal_record( row )
      for row in rows
   ]
