from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class TransportationRouteLegMarkerRecord:
   from_station: str
   to_station: str
   marker_id: str
