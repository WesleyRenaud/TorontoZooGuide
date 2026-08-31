from __future__ import annotations

from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.enclosure_viewing_walk_node_builder import EnclosureViewingWalkNodeBuilder


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

ANTELOPE_OUTDOOR_ROW = {
   'species': 'Antelope',
   'exhibit': 'Africa Savanna',
   'enclosure_type': 'Outdoor',
   'x_coord': 90.0,
   'y_coord': 90.0,
}

ZEBRA_OUTDOOR_ROW = {
   'species': 'Zebra',
   'exhibit': 'Africa Savanna',
   'enclosure_type': 'Outdoor',
   'x_coord': 10.0,
   'y_coord': 10.0,
}

OVERRIDE_ROW = {
   'species': 'Tortoise',
   'exhibit': 'Pavilion',
   'enclosure_type': 'Outdoor',
   'x_coord': 10.0,
   'y_coord': 10.0,
   'walk_node_id': 'n-2',
}


def Test_Build_TestNearestNode_ExpectSnappedWalkNode() -> None:
   rows = EnclosureViewingWalkNodeBuilder.build(
      TEST_GRAPH,
      [ ZEBRA_OUTDOOR_ROW ] )

   assert rows == [
      {
         'species': 'Zebra',
         'exhibit': 'Africa Savanna',
         'enclosure_type': 'Outdoor',
         'x': 10.0,
         'y': 10.0,
         'walk_node_id': 'n-1',
         'snap_distance_px': 0.0,
      },
   ]


def Test_Build_TestWalkNodeOverride_ExpectUsesOverrideAndDistance() -> None:
   rows = EnclosureViewingWalkNodeBuilder.build(
      TEST_GRAPH,
      [ OVERRIDE_ROW ] )

   assert rows == [
      {
         'species': 'Tortoise',
         'exhibit': 'Pavilion',
         'enclosure_type': 'Outdoor',
         'x': 10.0,
         'y': 10.0,
         'walk_node_id': 'n-2',
         'snap_distance_px': 113.137,
      },
   ]


def Test_Build_TestMultipleRows_ExpectSortedBySpeciesAndExhibit() -> None:
   rows = EnclosureViewingWalkNodeBuilder.build(
      TEST_GRAPH,
      [ ZEBRA_OUTDOOR_ROW, ANTELOPE_OUTDOOR_ROW ] )

   assert [ row[ 'species' ] for row in rows ] == [ 'Antelope', 'Zebra' ]
   assert rows[ 1 ][ 'walk_node_id' ] == 'n-1'
   assert rows[ 0 ][ 'walk_node_id' ] == 'n-2'
