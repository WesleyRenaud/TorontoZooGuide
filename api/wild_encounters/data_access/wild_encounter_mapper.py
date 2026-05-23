from __future__ import annotations

from collections.abc import Iterable

from ...types import Row
from .wild_encounter_record import WildEncounterRecord


def map_wild_encounter_record( row: Row ) -> WildEncounterRecord:
   return WildEncounterRecord(
      name=row[ 'NAME' ],
      meeting_spot=row[ 'MEETING_SPOT' ],
      link=row[ 'LINK' ],
      maximum_duration=row[ 'MAXIMUM_DURATION' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_wild_encounter_records( rows: Iterable[ Row ] ) -> list[ WildEncounterRecord ]:
   return [
      map_wild_encounter_record( row )
      for row in rows
   ]
