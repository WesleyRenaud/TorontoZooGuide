from __future__ import annotations

from ...types import Row
from .wild_encounter_cancellation_record import WildEncounterCancellationRecord


class WildEncounterCancellationMapper():
   @classmethod
   def map_record( cls, row: Row ) -> WildEncounterCancellationRecord:
      return WildEncounterCancellationRecord(
         cancellation_date=row[ 'CANCELLATION_DATE' ],
         encounter_time=row[ 'ENCOUNTER_TIME' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ WildEncounterCancellationRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
