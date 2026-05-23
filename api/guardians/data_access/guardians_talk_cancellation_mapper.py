from __future__ import annotations

from collections.abc import Iterable

from .guardians_talk_cancellation_record import GuardiansTalkCancellationRecord
from ...types import Row


def map_guardians_talk_cancellation_record( row: Row ) -> GuardiansTalkCancellationRecord:
   return GuardiansTalkCancellationRecord(
      cancellation_date=row[ 'CANCELLATION_DATE' ],
      talk_time=row[ 'TALK_TIME' ] )


def map_guardians_talk_cancellation_records(
      rows: Iterable[ Row ] ) -> list[ GuardiansTalkCancellationRecord ]:
   return [
      map_guardians_talk_cancellation_record( row )
      for row in rows
   ]
