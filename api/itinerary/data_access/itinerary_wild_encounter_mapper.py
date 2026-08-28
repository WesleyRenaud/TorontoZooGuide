from __future__ import annotations

from .itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from ...shared.value_conversion import ValueConversion
from ...types import Types


class ItineraryWildEncounterMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> ItineraryWildEncounterRecord:
      return ItineraryWildEncounterRecord(
         wild_encounter=row[ 'WILD_ENCOUNTER' ],
         start_time=row[ 'START_TIME' ],
         end_time=row[ 'END_TIME' ],
         is_deleted=ValueConversion.as_boolean( row[ 'IS_DELETED' ] ) )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ ItineraryWildEncounterRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
