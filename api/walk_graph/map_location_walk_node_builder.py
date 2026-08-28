from __future__ import annotations

from .domain.map_location_kind import MapLocationKind
from .domain.map_location_walk_node import MapLocationWalkNode
from .domain.walk_graph import WalkGraph
from .walk_node_snapper import WalkNodeSnapper


class MapLocationWalkNodeBuilder():
   @classmethod
   def build(
         cls,
         graph: WalkGraph,
         wild_encounter_meeting_spot_rows: list[ dict[ str, object ] ],
         guardians_talk_rows: list[ dict[ str, object ] ],
         attraction_rows: list[ dict[ str, object ] ] ) -> list[ MapLocationWalkNode ]:
      rows: list[ MapLocationWalkNode ] = []

      rows.extend(
         cls._rows_for_source(
            graph,
            MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT,
            wild_encounter_meeting_spot_rows ) )
      rows.extend(
         cls._rows_for_source(
            graph,
            MapLocationKind.GUARDIANS_TALK,
            guardians_talk_rows ) )
      rows.extend(
         cls._rows_for_source(
            graph,
            MapLocationKind.ATTRACTION,
            attraction_rows ) )

      rows.sort( key=lambda row: row.sort_key() )

      return rows


   @classmethod
   def _rows_for_source(
         cls,
         graph: WalkGraph,
         kind: MapLocationKind,
         source_rows: list[ dict[ str, object ] ] ) -> list[ MapLocationWalkNode ]:
      rows: list[ MapLocationWalkNode ] = []

      for source_row in source_rows:
         name = str( source_row[ 'name' ] )
         location = str( source_row.get( 'location', '' ) or '' )
         x_percent = float( source_row[ 'x_coord' ] )
         y_percent = float( source_row[ 'y_coord' ] )
         walk_node_id, snap_distance_px = WalkNodeSnapper.snap(
            x_percent,
            y_percent,
            graph )

         rows.append( MapLocationWalkNode(
            kind=kind,
            name=name,
            location=location,
            x=x_percent,
            y=y_percent,
            walk_node_id=walk_node_id,
            snap_distance_px=round( snap_distance_px, 3 ),
         ) )

      return rows
