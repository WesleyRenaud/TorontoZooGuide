from __future__ import annotations

from typing import Protocol


class TransportationLegStations( Protocol ):
   from_station: str
   to_station: str
