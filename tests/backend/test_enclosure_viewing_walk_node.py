from __future__ import annotations

import json
from pathlib import Path

from api.walk_graph.build_enclosure_viewing_walk_nodes import build_enclosure_viewing_walk_nodes
from api.walk_graph.data_access.load_enclosure_viewing_walk_nodes import load_enclosure_viewing_walk_nodes
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.data_access.paths import MAX_ENCLOSURE_VIEWING_SNAP_DISTANCE_PX
from api.walk_graph.domain.viewing_spot_key import viewing_spot_key_from_enclosure_viewing_row
from api.walk_graph.enclosure_viewing_walk_node_lookup import walk_node_id_by_enclosure_name
from api.walk_graph.enclosure_viewing_walk_node_lookup import walk_nodes_for_species_exhibit


ROOT = Path( __file__ ).resolve().parents[ 2 ]
ENCLOSURE_VIEWING_PATH = ROOT / 'api' / 'seed' / 'data' / 'enclosure_viewing.json'


def test_enclosure_viewing_walk_nodes_cover_every_viewing_spot() -> None:
   enclosure_viewing_rows = json.loads(
      ENCLOSURE_VIEWING_PATH.read_text( encoding='utf-8' ) )
   expected_keys = {
      viewing_spot_key_from_enclosure_viewing_row( row )
      for row in enclosure_viewing_rows
   }
   actual_keys = {
      ( row[ 'species' ], row[ 'exhibit' ], row[ 'x' ], row[ 'y' ] )
      for row in load_enclosure_viewing_walk_nodes()
   }

   assert len( load_enclosure_viewing_walk_nodes() ) == len( enclosure_viewing_rows )
   assert expected_keys == actual_keys


def test_enclosure_viewing_walk_nodes_reference_valid_walk_graph_nodes() -> None:
   graph = load_walk_graph()
   node_ids = { node[ 'id' ] for node in graph[ 'nodes' ] }

   for row in load_enclosure_viewing_walk_nodes():
      assert row[ 'walk_node_id' ] in node_ids
      assert row[ 'snap_distance_px' ] >= 0
      assert row[ 'snap_distance_px' ] <= MAX_ENCLOSURE_VIEWING_SNAP_DISTANCE_PX
      assert row[ 'enclosure_type' ] in { 'Indoor', 'Outdoor' }


def test_enclosure_viewing_walk_nodes_match_nearest_node_snap() -> None:
   graph = load_walk_graph()
   enclosure_viewing_rows = json.loads(
      ENCLOSURE_VIEWING_PATH.read_text( encoding='utf-8' ) )
   expected_rows = build_enclosure_viewing_walk_nodes(
      graph,
      enclosure_viewing_rows )

   assert load_enclosure_viewing_walk_nodes() == expected_rows


def test_walk_nodes_for_species_exhibit_returns_every_viewing_spot() -> None:
   gorilla_rows = walk_nodes_for_species_exhibit(
      'Western Lowland Gorilla',
      'African Rainforest Pavilion' )
   kudu_rows = walk_nodes_for_species_exhibit(
      'Greater Kudu',
      'Africa Savanna' )

   assert len( gorilla_rows ) == 2
   assert { row[ 'enclosure_type' ] for row in gorilla_rows } == { 'Indoor', 'Outdoor' }
   assert len( kudu_rows ) == 3
   assert all( row[ 'enclosure_type' ] == 'Outdoor' for row in kudu_rows )
   assert len( { row[ 'walk_node_id' ] for row in kudu_rows } ) == 3


def test_walk_node_id_by_enclosure_name_resolves_viewing_spot_name() -> None:
   walk_node_ids = walk_node_id_by_enclosure_name()

   assert walk_node_ids[
      ( 'Ostrich', 'Africa Savanna', None )
   ] == 'v-0426'

   assert walk_node_ids[
      ( 'Ostrich', 'Africa Savanna', 'Savanna Overlook' )
   ] == 'v-0263'
