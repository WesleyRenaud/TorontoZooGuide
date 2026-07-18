from __future__ import annotations

from .itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from ...shared.value_conversion import ValueConversion
from ...types import Row


def map_itinerary_wild_encounter_record( row: Row ) -> ItineraryWildEncounterRecord:
   return ItineraryWildEncounterRecord(
      wild_encounter=row[ 'WILD_ENCOUNTER' ],
      start_time=row[ 'START_TIME' ],
      end_time=row[ 'END_TIME' ],
      is_deleted=ValueConversion.as_boolean( row[ 'IS_DELETED' ] ) )


def map_itinerary_wild_encounter_records( rows: list[ Row ] ) -> list[ ItineraryWildEncounterRecord ]:
   return [
      map_itinerary_wild_encounter_record( row )
      for row in rows
   ]
