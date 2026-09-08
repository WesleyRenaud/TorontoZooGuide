from __future__ import annotations

from api.shared.enums.position import Position
from api.walk_graph.domain.map_location_kind import MapLocationKind
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.map_location_walk_node_builder import MapLocationWalkNodeBuilder


TEST_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': 'n-1',
   'nodes': [
      { 'id': 'n-1', 'x_px': 10.0, 'y_px': 10.0 },
      { 'id': 'n-2', 'x_px': 90.0, 'y_px': 90.0 },
   ],
   'edges': [],
}

CAROUSEL_ROW = {
   'name': 'Carousel',
   'x_coord': 90.0,
   'y_coord': 90.0,
}

KOMODO_TALK_ROW = {
   'name': 'Komodo Dragon',
   'location': 'Indo-Malaya',
   'x_coord': 10.0,
   'y_coord': 10.0,
}

RHINO_MEETING_SPOT_ROW = {
   'name': 'White Rhino',
   'x_coord': 90.0,
   'y_coord': 10.0,
}


def Test_Build_TestAttractionRow_ExpectSnappedWalkNode() -> None:
   rows = MapLocationWalkNodeBuilder.build(
      TEST_GRAPH,
      wild_encounter_meeting_spot_rows=[],
      guardians_talk_rows=[],
      attraction_rows=[ CAROUSEL_ROW ] )

   assert len( rows ) == 1
   assert rows[ Position.FIRST ].kind == MapLocationKind.ATTRACTION
   assert rows[ Position.FIRST ].name == 'Carousel'
   assert rows[ Position.FIRST ].walk_node_id == 'n-2'
   assert rows[ Position.FIRST ].snap_distance_px == 0.0


def Test_Build_TestGuardiansTalkRow_ExpectLocationPreserved() -> None:
   rows = MapLocationWalkNodeBuilder.build(
      TEST_GRAPH,
      wild_encounter_meeting_spot_rows=[],
      guardians_talk_rows=[ KOMODO_TALK_ROW ],
      attraction_rows=[] )

   assert len( rows ) == 1
   assert rows[ Position.FIRST ].kind == MapLocationKind.GUARDIANS_TALK
   assert rows[ Position.FIRST ].name == 'Komodo Dragon'
   assert rows[ Position.FIRST ].location == 'Indo-Malaya'
   assert rows[ Position.FIRST ].walk_node_id == 'n-1'


def Test_Build_TestMixedRows_ExpectSortedByKindAndName() -> None:
   rows = MapLocationWalkNodeBuilder.build(
      TEST_GRAPH,
      wild_encounter_meeting_spot_rows=[ RHINO_MEETING_SPOT_ROW ],
      guardians_talk_rows=[ KOMODO_TALK_ROW ],
      attraction_rows=[ CAROUSEL_ROW ] )

   assert [ ( row.kind, row.name ) for row in rows ] == [
      ( MapLocationKind.ATTRACTION, 'Carousel' ),
      ( MapLocationKind.GUARDIANS_TALK, 'Komodo Dragon' ),
      ( MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT, 'White Rhino' ),
   ]
