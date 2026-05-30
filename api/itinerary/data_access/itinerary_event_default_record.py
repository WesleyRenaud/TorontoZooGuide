from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import ItineraryEventType


@dataclass( frozen=True )
class ItineraryEventDefaultRecord:
   event_type: ItineraryEventType
   default_duration_minutes: int
