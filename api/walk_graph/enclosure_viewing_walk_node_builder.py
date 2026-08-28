from __future__ import annotations

from .domain.enclosure_viewing_walk_node import EnclosureViewingWalkNode
from .domain.walk_graph import WalkGraph
from .walk_node_snapper import WalkNodeSnapper


class EnclosureViewingWalkNodeBuilder():
   @classmethod
   def build(
         cls,
         graph: WalkGraph,
         enclosure_viewing_rows: list[ dict[ str, object ] ] ) -> list[ EnclosureViewingWalkNode ]:
      rows: list[ EnclosureViewingWalkNode ] = []

      for enclosure_viewing_row in enclosure_viewing_rows:
         species = str( enclosure_viewing_row[ 'species' ] )
         exhibit = str( enclosure_viewing_row[ 'exhibit' ] )
         enclosure_type = str( enclosure_viewing_row[ 'enclosure_type' ] )
         x_percent = float( enclosure_viewing_row[ 'x_coord' ] )
         y_percent = float( enclosure_viewing_row[ 'y_coord' ] )
         walk_node_id_override = enclosure_viewing_row.get( 'walk_node_id' )

         if walk_node_id_override is not None:
            walk_node_id = str( walk_node_id_override )
            snap_distance_px = WalkNodeSnapper.distance(
               x_percent,
               y_percent,
               walk_node_id,
               graph )
         else:
            walk_node_id, snap_distance_px = WalkNodeSnapper.snap(
               x_percent,
               y_percent,
               graph )

         rows.append( {
            'species': species,
            'exhibit': exhibit,
            'enclosure_type': enclosure_type,
            'x': x_percent,
            'y': y_percent,
            'walk_node_id': walk_node_id,
            'snap_distance_px': round( snap_distance_px, 3 ),
         } )

      rows.sort(
         key=lambda row: (
            row[ 'species' ].lower(),
            row[ 'exhibit' ].lower(),
         ) )

      return rows
