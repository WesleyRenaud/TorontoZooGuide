from __future__ import annotations

import json
from pathlib import Path

from api.walk_graph.data_access.enclosure_viewing_walk_node_provider import EnclosureViewingWalkNodeProvider
from api.walk_graph.data_access.paths import MAX_ENCLOSURE_VIEWING_SNAP_DISTANCE_PX
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.domain.viewing_spot_key import viewing_spot_key_from_enclosure_viewing_row
from api.walk_graph.enclosure_viewing_walk_node_builder import EnclosureViewingWalkNodeBuilder
from api.walk_graph.enclosure_viewing_walk_node_lookup import EnclosureViewingWalkNodeLookup
from api.walk_graph.enclosure_viewing_walk_node_lookup import EnclosureViewingWalkNodeLookup


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
      for row in EnclosureViewingWalkNodeProvider.fetch_records()
   }

   assert len( EnclosureViewingWalkNodeProvider.fetch_records() ) == len( enclosure_viewing_rows )
   assert expected_keys == actual_keys


def test_enclosure_viewing_walk_nodes_reference_valid_walk_graph_nodes() -> None:
   graph = WalkGraphProvider.fetch()
   node_ids = { node[ 'id' ] for node in graph[ 'nodes' ] }

   for row in EnclosureViewingWalkNodeProvider.fetch_records():
      assert row[ 'walk_node_id' ] in node_ids
      assert row[ 'snap_distance_px' ] >= 0
      assert row[ 'snap_distance_px' ] <= MAX_ENCLOSURE_VIEWING_SNAP_DISTANCE_PX
      assert row[ 'enclosure_type' ] in { 'Indoor', 'Outdoor' }


def test_enclosure_viewing_walk_nodes_match_nearest_node_snap() -> None:
   graph = WalkGraphProvider.fetch()
   enclosure_viewing_rows = json.loads(
      ENCLOSURE_VIEWING_PATH.read_text( encoding='utf-8' ) )
   expected_rows = EnclosureViewingWalkNodeBuilder.build(
      graph,
      enclosure_viewing_rows )

   assert EnclosureViewingWalkNodeProvider.fetch_records() == expected_rows


def test_walk_nodes_for_species_exhibit_returns_every_viewing_spot() -> None:
   gorilla_rows = EnclosureViewingWalkNodeLookup.for_species_exhibit(
      'Western Lowland Gorilla',
      'African Rainforest Pavilion' )
   kudu_rows = EnclosureViewingWalkNodeLookup.for_species_exhibit(
      'Greater Kudu',
      'Africa Savanna' )
   kudu_pavilion_rows = EnclosureViewingWalkNodeLookup.for_species_exhibit(
      'Greater Kudu',
      'African Rainforest Pavilion' )

   assert len( gorilla_rows ) == 2
   assert { row[ 'enclosure_type' ] for row in gorilla_rows } == { 'Indoor', 'Outdoor' }
   assert len( kudu_rows ) == 2
   assert all( row[ 'enclosure_type' ] == 'Outdoor' for row in kudu_rows )
   assert len( { row[ 'walk_node_id' ] for row in kudu_rows } ) == 2
   assert len( kudu_pavilion_rows ) == 1
   assert kudu_pavilion_rows[ 0 ][ 'walk_node_id' ] == 'v-0263'
   zebra_savanna_rows = EnclosureViewingWalkNodeLookup.for_species_exhibit(
      "Grevy's Zebra",
      'Africa Savanna' )
   zebra_domain_rows = EnclosureViewingWalkNodeLookup.for_species_exhibit(
      "Grevy's Zebra",
      'Canadian Domain' )

   assert len( zebra_savanna_rows ) == 1
   assert len( zebra_domain_rows ) == 1
   assert zebra_domain_rows[ 0 ][ 'walk_node_id' ] == 'v-0457'


def test_walk_node_id_by_enclosure_name_resolves_viewing_spot_name() -> None:
   walk_node_ids = EnclosureViewingWalkNodeLookup.walk_node_id_by_enclosure_name()

   assert walk_node_ids[
      ( 'Ostrich', 'Africa Savanna', None )
   ] == 'v-0426'

   assert walk_node_ids[
      ( 'Ostrich', 'African Rainforest Pavilion', 'Savanna Overlook' )
   ] == 'v-0263'
