from __future__ import annotations

from .master_route_loop import MasterRouteLoop
from .master_route_stop_mapper import MasterRouteStopMapper


class MasterRouteLoopMapper():
   @classmethod
   def map_record( cls, payload: dict[ str, object ] ) -> MasterRouteLoop:
      return MasterRouteLoop(
         loop_id=str( payload[ 'id' ] ),
         name=str( payload[ 'name' ] ),
         traversal=str( payload[ 'traversal' ] ),
         viewing_spots=[
            MasterRouteStopMapper.map_record( row )
            for row in payload.get( 'viewing_spots', [] )
         ] )
