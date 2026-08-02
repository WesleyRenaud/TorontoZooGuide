from __future__ import annotations

from .guardians_talk_occurrence_record import GuardiansTalkOccurrenceRecord
from ...types import Row


def map_guardians_talk_occurrence_record( row: Row ) -> GuardiansTalkOccurrenceRecord:
   return GuardiansTalkOccurrenceRecord(
      occurrence_date=row[ 'OCCURRENCE_DATE' ],
      talk_time=row[ 'TALK_TIME' ] )


def map_guardians_talk_occurrence_records(
      rows: list[ Row ] ) -> list[ GuardiansTalkOccurrenceRecord ]:
   return [
      map_guardians_talk_occurrence_record( row )
      for row in rows
   ]
