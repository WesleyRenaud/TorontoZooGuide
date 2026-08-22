from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class ItineraryTransportationRouteMarkerRecord:
   transportation: str
   sequence: int
   marker_order: int
   marker_id: str
