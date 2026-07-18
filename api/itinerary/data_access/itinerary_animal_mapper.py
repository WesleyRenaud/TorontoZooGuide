from __future__ import annotations

from .itinerary_animal_record import ItineraryAnimalRecord
from ...shared.value_conversion import ValueConversion
from ...types import Row


def map_itinerary_animal_record( row: Row ) -> ItineraryAnimalRecord:
   return ItineraryAnimalRecord(
      species=row[ 'SPECIES' ],
      exhibit=row[ 'EXHIBIT' ],
      enclosure_name=row[ 'ENCLOSURE_NAME' ],
      old_likelihood=row[ 'OLD_LIKELIHOOD' ],
      new_likelihood=row[ 'NEW_LIKELIHOOD' ],
      is_added=ValueConversion.as_boolean( row[ 'IS_ADDED' ] ),
      covered_by_talk=ValueConversion.as_boolean( row[ 'COVERED_BY_TALK' ] ),
      start_time=row[ 'START_TIME' ],
      end_time=row[ 'END_TIME' ] )


def map_itinerary_animal_records( rows: list[ Row ] ) -> list[ ItineraryAnimalRecord ]:
   return [
      map_itinerary_animal_record( row )
      for row in rows
   ]
