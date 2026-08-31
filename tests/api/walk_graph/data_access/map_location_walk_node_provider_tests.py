from __future__ import annotations

import json
from pathlib import Path

from api.walk_graph.data_access.map_location_walk_node_provider import MapLocationWalkNodeProvider
from api.walk_graph.domain.map_location_kind import MapLocationKind
from api.walk_graph.domain.map_location_walk_node import MapLocationWalkNode


ATTRACTION_RECORD = MapLocationWalkNode(
   kind=MapLocationKind.ATTRACTION,
   name='Carousel',
   location='',
   x=90.0,
   y=90.0,
   walk_node_id='n-5002',
   snap_distance_px=0.0,
)

GUARDIANS_TALK_RECORD = MapLocationWalkNode(
   kind=MapLocationKind.GUARDIANS_TALK,
   name='Komodo Dragon',
   location='Indo-Malaya',
   x=10.0,
   y=10.0,
   walk_node_id='n-5001',
   snap_distance_px=0.0,
)

PROVIDER_RECORDS = [ ATTRACTION_RECORD, GUARDIANS_TALK_RECORD ]


def Test_FetchRecords_TestJsonFiles_ExpectParsedAndSortedRecords( tmp_path: Path ) -> None:
   attraction_path = tmp_path / 'attraction_walk_nodes.json'
   guardians_talk_path = tmp_path / 'guardians_talk_walk_nodes.json'
   attraction_path.write_text(
      json.dumps( [ ATTRACTION_RECORD.to_json() ] ),
      encoding='utf-8' )
   guardians_talk_path.write_text(
      json.dumps( [ GUARDIANS_TALK_RECORD.to_json() ] ),
      encoding='utf-8' )

   assert MapLocationWalkNodeProvider.fetch_records(
      paths=[ guardians_talk_path, attraction_path ] ) == PROVIDER_RECORDS
