from __future__ import annotations

from collections import defaultdict

from .domain.walk_graph import WalkGraph
from .shortest_path import WalkGraphAdjacency


class WalkGraphAdjacencyBuilder():
   @classmethod
   def build( cls, graph: WalkGraph ) -> WalkGraphAdjacency:
      adjacency: WalkGraphAdjacency = defaultdict( list )

      for edge in graph[ 'edges' ]:
         from_id = str( edge[ 'from' ] )
         to_id = str( edge[ 'to' ] )
         length_px = float( edge[ 'length_px' ] )

         adjacency[ from_id ].append( ( to_id, length_px ) )

      return dict( adjacency )
