from __future__ import annotations

from collections.abc import Iterable

from ...types import Row
from .itinerary_animal_record import ItineraryAnimalRecord


def map_itinerary_animal_record( row: Row ) -> ItineraryAnimalRecord:
   return ItineraryAnimalRecord(
      species=row[ 'SPECIES' ],
      exhibit=row[ 'EXHIBIT' ],
      old_likelihood=row[ 'OLD_LIKELIHOOD' ],
      new_likelihood=row[ 'NEW_LIKELIHOOD' ] )


def map_itinerary_animal_records( rows: Iterable[ Row ] ) -> list[ ItineraryAnimalRecord ]:
   return [
      map_itinerary_animal_record( row )
      for row in rows
   ]
