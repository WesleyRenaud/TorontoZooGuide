from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class GuardiansTalkCancellationRecord:
   cancellation_date: str
   talk_time: str
