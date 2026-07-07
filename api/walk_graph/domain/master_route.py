from __future__ import annotations

from dataclasses import dataclass

from .master_route_loop import master_route_loop_from_json
from .master_route_loop import MasterRouteLoop


@dataclass( frozen=True )
class MasterRoute:
   route_id: str
   description: str
   loops: tuple[ MasterRouteLoop, ... ]


def master_route_from_json( payload: dict[ str, object ] ) -> MasterRoute:
   return MasterRoute(
      route_id=str( payload[ 'id' ] ),
      description=str( payload.get( 'description', '' ) ),
      loops=tuple(
         master_route_loop_from_json( loop )
         for loop in payload[ 'loops' ] ) )
