from __future__ import annotations

import json
from pathlib import Path

from api.walk_graph.build_map_location_walk_nodes import build_map_location_walk_nodes
from api.walk_graph.data_access.load_map_location_walk_nodes import load_map_location_walk_nodes
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.data_access.paths import MAX_MAP_LOCATION_SNAP_DISTANCE_PX
from api.walk_graph.domain.map_location_key import MapLocationKey
from api.walk_graph.domain.map_location_kind import MapLocationKind
from api.walk_graph.map_location_walk_node_lookup import walk_node_for_map_location


ROOT = Path( __file__ ).resolve().parents[ 2 ]
SEED_DATA_DIR = ROOT / 'api' / 'seed' / 'data'


def _expected_map_location_keys() -> set[ MapLocationKey ]:
   wild_encounter_meeting_spots = json.loads(
      ( SEED_DATA_DIR / 'wild_encounter_meeting_spot.json' ).read_text( encoding='utf-8' ) )
   guardians_talks = json.loads(
      ( SEED_DATA_DIR / 'meet_the_guardians_talk.json' ).read_text( encoding='utf-8' ) )
   attractions = json.loads(
      ( SEED_DATA_DIR / 'attraction.json' ).read_text( encoding='utf-8' ) )

   expected_keys = {
      MapLocationKey.for_kind(
         MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT,
         row[ 'name' ] )
      for row in wild_encounter_meeting_spots
   }
   expected_keys.update(
      MapLocationKey.for_kind(
         MapLocationKind.GUARDIANS_TALK,
         row[ 'name' ],
         location=str( row.get( 'location', '' ) or '' ),
      )
      for row in guardians_talks )
   expected_keys.update(
      MapLocationKey.for_kind(
         MapLocationKind.ATTRACTION,
         row[ 'name' ] )
      for row in attractions )

   return expected_keys


def test_map_location_walk_nodes_cover_every_seed_location() -> None:
   expected_keys = _expected_map_location_keys()
   actual_keys = {
      row.location_key()
      for row in load_map_location_walk_nodes()
   }

   assert len( load_map_location_walk_nodes() ) == len( expected_keys )
   assert expected_keys == actual_keys


def test_map_location_walk_nodes_reference_valid_walk_graph_nodes() -> None:
   graph = load_walk_graph()
   node_ids = { node[ 'id' ] for node in graph[ 'nodes' ] }

   for row in load_map_location_walk_nodes():
      assert row.walk_node_id in node_ids
      assert row.snap_distance_px >= 0
      assert row.snap_distance_px <= MAX_MAP_LOCATION_SNAP_DISTANCE_PX


def test_map_location_walk_nodes_match_nearest_node_snap() -> None:
   graph = load_walk_graph()
   expected_rows = build_map_location_walk_nodes(
      graph,
      json.loads(
         ( SEED_DATA_DIR / 'wild_encounter_meeting_spot.json' ).read_text( encoding='utf-8' ) ),
      json.loads(
         ( SEED_DATA_DIR / 'meet_the_guardians_talk.json' ).read_text( encoding='utf-8' ) ),
      json.loads(
         ( SEED_DATA_DIR / 'attraction.json' ).read_text( encoding='utf-8' ) ) )

   assert load_map_location_walk_nodes() == expected_rows


def test_walk_node_for_map_location_finds_rhino_encounter_meeting_spot() -> None:
   row = walk_node_for_map_location(
      MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT,
      'Wild Encounter - Penguin Meeting Spot' )

   assert row is not None
   assert row.walk_node_id.startswith( 'v-' )
