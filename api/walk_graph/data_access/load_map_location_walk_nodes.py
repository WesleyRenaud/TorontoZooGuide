from __future__ import annotations

import json
from pathlib import Path

from ..domain.map_location_walk_node import MapLocationWalkNode
from .paths import MAP_LOCATION_WALK_NODE_PATHS


def load_map_location_walk_nodes(
      paths: tuple[ Path, ... ] = MAP_LOCATION_WALK_NODE_PATHS,
   ) -> list[ MapLocationWalkNode ]:
   rows: list[ MapLocationWalkNode ] = []

   for path in paths:
      for row in json.loads( path.read_text( encoding='utf-8' ) ):
         rows.append( MapLocationWalkNode.from_json( row ) )

   rows.sort( key=lambda row: row.sort_key() )

   return rows
