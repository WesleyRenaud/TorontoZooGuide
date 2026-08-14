from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class TransportationRouteRecord:
   transportation: str
   route: str
