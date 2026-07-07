from __future__ import annotations

from dataclasses import dataclass

from .viewing_spot_reference import viewing_spot_reference_from_json
from .viewing_spot_reference import ViewingSpotReference


MasterRouteTraversal = str


@dataclass( frozen=True )
class MasterRouteLoop:
   loop_id: str
   name: str
   traversal: MasterRouteTraversal
   viewing_spots: tuple[ ViewingSpotReference, ... ]


def master_route_loop_from_json(
      payload: dict[ str, object ] ) -> MasterRouteLoop:
   return MasterRouteLoop(
      loop_id=str( payload[ 'id' ] ),
      name=str( payload[ 'name' ] ),
      traversal=str( payload[ 'traversal' ] ),
      viewing_spots=tuple(
         viewing_spot_reference_from_json( row )
         for row in payload[ 'viewing_spots' ] ) )
