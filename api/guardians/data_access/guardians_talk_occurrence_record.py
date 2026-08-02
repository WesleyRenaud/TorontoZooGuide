from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class GuardiansTalkOccurrenceRecord:
   occurrence_date: str
   talk_time: str
