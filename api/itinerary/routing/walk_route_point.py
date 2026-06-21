from __future__ import annotations

from dataclasses import dataclass

from ...walk_graph.domain.walk_graph_node import WalkGraphNode


@dataclass( frozen=True )
class WalkRoutePoint:
   node_id: str
   x: float
   y: float
   x_px: float
   y_px: float

   @classmethod
   def from_walk_graph_node( cls, node: WalkGraphNode ) -> WalkRoutePoint:
      return cls(
         node_id=str( node[ 'id' ] ),
         x=float( node[ 'x' ] ),
         y=float( node[ 'y' ] ),
         x_px=float( node[ 'x_px' ] ),
         y_px=float( node[ 'y_px' ] ) )


   def to_dict( self ) -> dict[ str, float | str ]:
      return {
         'node_id': self.node_id,
         'x': self.x,
         'y': self.y,
         'x_px': self.x_px,
         'y_px': self.y_px,
      }
