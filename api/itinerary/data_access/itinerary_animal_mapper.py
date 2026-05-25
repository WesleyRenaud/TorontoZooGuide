from __future__ import annotations

from collections.abc import Iterable

from .itinerary_animal_record import ItineraryAnimalRecord
from ...shared.value_conversion import ValueConversion
from ...types import Row


def map_itinerary_animal_record( row: Row ) -> ItineraryAnimalRecord:
   return ItineraryAnimalRecord(
      species=row[ 'SPECIES' ],
      exhibit=row[ 'EXHIBIT' ],
      old_likelihood=row[ 'OLD_LIKELIHOOD' ],
      new_likelihood=row[ 'NEW_LIKELIHOOD' ],
      is_added=ValueConversion.as_boolean( row[ 'IS_ADDED' ] ) )


def map_itinerary_animal_records( rows: Iterable[ Row ] ) -> list[ ItineraryAnimalRecord ]:
   return [
      map_itinerary_animal_record( row )
      for row in rows
   ]
