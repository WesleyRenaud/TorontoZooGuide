from __future__ import annotations

import json
from pathlib import Path

from api.walk_graph.data_access.enclosure_viewing_walk_node_provider import EnclosureViewingWalkNodeProvider
from api.walk_graph.domain.enclosure_viewing_walk_node import EnclosureViewingWalkNode


PROVIDER_RECORDS: list[ EnclosureViewingWalkNode ] = [
   {
      'species': 'Antelope',
      'exhibit': 'Africa Savanna',
      'enclosure_type': 'Outdoor',
      'x': 30.0,
      'y': 40.0,
      'walk_node_id': 'n-2001',
      'snap_distance_px': 0.0,
   },
   {
      'species': 'Zebra',
      'exhibit': 'Africa Savanna',
      'enclosure_type': 'Outdoor',
      'x': 31.0,
      'y': 41.0,
      'walk_node_id': 'n-2002',
      'snap_distance_px': 1.5,
   },
]


def Test_FetchRecords_TestJsonFile_ExpectParsedRecords( tmp_path: Path ) -> None:
   records_path = tmp_path / 'enclosure_viewing_walk_node.json'
   records_path.write_text( json.dumps( PROVIDER_RECORDS ), encoding='utf-8' )

   assert EnclosureViewingWalkNodeProvider.fetch_records( path=records_path ) == PROVIDER_RECORDS
