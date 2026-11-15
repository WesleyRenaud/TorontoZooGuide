from __future__ import annotations

from dataclasses import dataclass

from .zoomobile_route_change import ZoomobileRouteChange


@dataclass( frozen=True )
class ZoomobileRoutePlan:
   writes: list[ ZoomobileRouteChange ]
   change: ZoomobileRouteChange | None
   added: bool


   def count( self ) -> int:
      return len( self.writes )
