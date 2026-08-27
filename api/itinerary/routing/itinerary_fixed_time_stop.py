from __future__ import annotations

from dataclasses import dataclass

from .itinerary_stop import ItineraryStop


@dataclass( frozen=True )
class ItineraryFixedTimeStop:
   stop: ItineraryStop
   start_seconds: int
   end_seconds: int
