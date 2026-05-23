from __future__ import annotations

from collections.abc import Iterable

from ... import zoo
from ...types import Row
from .itinerary_wild_encounter_record import ItineraryWildEncounterRecord


def map_itinerary_wild_encounter_record( row: Row ) -> ItineraryWildEncounterRecord:
   return ItineraryWildEncounterRecord(
      wild_encounter=row[ 'WILD_ENCOUNTER' ],
      start_time=row[ 'START_TIME' ],
      end_time=row[ 'END_TIME' ],
      is_deleted=zoo.ZooUtil.as_boolean( row[ 'IS_DELETED' ] ) )


def map_itinerary_wild_encounter_records( rows: Iterable[ Row ] ) -> list[ ItineraryWildEncounterRecord ]:
   return [
      map_itinerary_wild_encounter_record( row )
      for row in rows
   ]
