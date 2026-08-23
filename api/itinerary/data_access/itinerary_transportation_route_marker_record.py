from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class ItineraryTransportationRouteMarkerRecord:
   transportation: str
   added_as_attraction: bool
   sequence: int
   marker_order: int
   marker_id: str
