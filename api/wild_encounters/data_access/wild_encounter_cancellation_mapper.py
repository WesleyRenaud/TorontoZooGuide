from __future__ import annotations

from collections.abc import Iterable

from ...types import Row
from .wild_encounter_cancellation_record import WildEncounterCancellationRecord


def map_wild_encounter_cancellation_record( row: Row ) -> WildEncounterCancellationRecord:
   return WildEncounterCancellationRecord(
      cancellation_date=row[ 'CANCELLATION_DATE' ],
      encounter_time=row[ 'ENCOUNTER_TIME' ] )


def map_wild_encounter_cancellation_records( rows: Iterable[ Row ] ) -> list[ WildEncounterCancellationRecord ]:
   return [
      map_wild_encounter_cancellation_record( row )
      for row in rows
   ]
