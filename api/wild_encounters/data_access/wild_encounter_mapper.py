from __future__ import annotations

from ...types import Types
from .wild_encounter_record import WildEncounterRecord


class WildEncounterMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> WildEncounterRecord:
      return WildEncounterRecord(
         name=row[ 'NAME' ],
         meeting_spot=row[ 'MEETING_SPOT' ],
         link=row[ 'LINK' ],
         maximum_duration=row[ 'MAXIMUM_DURATION' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ],
         region=row[ 'REGION' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ WildEncounterRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
