from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class GuardiansTalkOccurrenceInput:
   talk_name: str
   location: str
   occurrence_date: str
   talk_time: str
