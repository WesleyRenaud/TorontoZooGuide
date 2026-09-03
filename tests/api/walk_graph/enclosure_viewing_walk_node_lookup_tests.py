from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from api.walk_graph.data_access.enclosure_viewing_walk_node_provider import EnclosureViewingWalkNodeProvider
from api.walk_graph.domain.enclosure_viewing_walk_node import EnclosureViewingWalkNode
from api.walk_graph.enclosure_viewing_walk_node_lookup import EnclosureViewingWalkNodeLookup


AFRICAN_RAINFOREST_PAVILION = 'African Rainforest Pavilion'
AFRICA_SAVANNA = 'Africa Savanna'
CANADIAN_DOMAIN = 'Canadian Domain'

GORILLA_INDOOR: EnclosureViewingWalkNode = {
   'species': 'Western Lowland Gorilla',
   'exhibit': AFRICAN_RAINFOREST_PAVILION,
   'enclosure_type': 'Indoor',
   'x': 10.0,
   'y': 20.0,
   'walk_node_id': 'v-1001',
   'snap_distance_px': 0.0,
}

GORILLA_OUTDOOR: EnclosureViewingWalkNode = {
   'species': 'Western Lowland Gorilla',
   'exhibit': AFRICAN_RAINFOREST_PAVILION,
   'enclosure_type': 'Outdoor',
   'x': 11.0,
   'y': 21.0,
   'walk_node_id': 'v-1002',
   'snap_distance_px': 0.0,
}

KUDU_SAVANNA_OUTDOOR_A: EnclosureViewingWalkNode = {
   'species': 'Greater Kudu',
   'exhibit': AFRICA_SAVANNA,
   'enclosure_type': 'Outdoor',
   'x': 30.0,
   'y': 40.0,
   'walk_node_id': 'v-2001',
   'snap_distance_px': 0.0,
}

KUDU_SAVANNA_OUTDOOR_B: EnclosureViewingWalkNode = {
   'species': 'Greater Kudu',
   'exhibit': AFRICA_SAVANNA,
   'enclosure_type': 'Outdoor',
   'x': 31.0,
   'y': 41.0,
   'walk_node_id': 'v-2002',
   'snap_distance_px': 0.0,
}

KUDU_PAVILION_OUTDOOR: EnclosureViewingWalkNode = {
   'species': 'Greater Kudu',
   'exhibit': AFRICAN_RAINFOREST_PAVILION,
   'enclosure_type': 'Outdoor',
   'x': 12.0,
   'y': 22.0,
   'walk_node_id': 'v-2003',
   'snap_distance_px': 0.0,
}

ZEBRA_SAVANNA: EnclosureViewingWalkNode = {
   'species': "Grevy's Zebra",
   'exhibit': AFRICA_SAVANNA,
   'enclosure_type': 'Outdoor',
   'x': 50.0,
   'y': 60.0,
   'walk_node_id': 'v-3001',
   'snap_distance_px': 0.0,
}

ZEBRA_DOMAIN: EnclosureViewingWalkNode = {
   'species': "Grevy's Zebra",
   'exhibit': CANADIAN_DOMAIN,
   'enclosure_type': 'Outdoor',
   'x': 51.0,
   'y': 61.0,
   'walk_node_id': 'v-3002',
   'snap_distance_px': 0.0,
}

OSTRICH_SAVANNA: EnclosureViewingWalkNode = {
   'species': 'Ostrich',
   'exhibit': AFRICA_SAVANNA,
   'enclosure_type': 'Outdoor',
   'x': 70.0,
   'y': 80.0,
   'walk_node_id': 'v-4001',
   'snap_distance_px': 0.0,
}

OSTRICH_PAVILION: EnclosureViewingWalkNode = {
   'species': 'Ostrich',
   'exhibit': AFRICAN_RAINFOREST_PAVILION,
   'enclosure_type': 'Outdoor',
   'x': 13.0,
   'y': 23.0,
   'walk_node_id': 'v-4002',
   'snap_distance_px': 0.0,
}

WALK_NODE_ROWS = [
   GORILLA_INDOOR,
   GORILLA_OUTDOOR,
   KUDU_SAVANNA_OUTDOOR_A,
   KUDU_SAVANNA_OUTDOOR_B,
   KUDU_PAVILION_OUTDOOR,
   ZEBRA_SAVANNA,
   ZEBRA_DOMAIN,
   OSTRICH_SAVANNA,
   OSTRICH_PAVILION,
]

ENCLOSURE_VIEWING_ROWS = [
   {
      'species': 'Ostrich',
      'exhibit': AFRICA_SAVANNA,
      'enclosure_type': 'Outdoor',
      'x_coord': 70.0,
      'y_coord': 80.0,
   },
   {
      'species': 'Ostrich',
      'exhibit': AFRICAN_RAINFOREST_PAVILION,
      'enclosure_type': 'Outdoor',
      'x_coord': 13.0,
      'y_coord': 23.0,
      'name': 'Savanna Overlook',
   },
]


def _clear_lookup_cache() -> None:
   EnclosureViewingWalkNodeLookup.by_viewing_spot.cache_clear()
   EnclosureViewingWalkNodeLookup.walk_node_id_by_enclosure_name.cache_clear()
   EnclosureViewingWalkNodeLookup.grouped_by_species_exhibit.cache_clear()


@pytest.fixture
def stub_enclosure_viewing_walk_nodes( monkeypatch: pytest.MonkeyPatch ) -> None:
   _clear_lookup_cache()
   monkeypatch.setattr(
      EnclosureViewingWalkNodeProvider,
      'fetch_records',
      lambda: WALK_NODE_ROWS )
   stub_path = MagicMock()
   stub_path.read_text.return_value = json.dumps( ENCLOSURE_VIEWING_ROWS )
   monkeypatch.setattr(
      'api.walk_graph.enclosure_viewing_walk_node_lookup.Paths.ENCLOSURE_VIEWING_PATH',
      stub_path )
   yield
   _clear_lookup_cache()


def Test_ForSpeciesExhibit_TestWesternLowlandGorilla_ExpectIndoorAndOutdoorSpots(
      stub_enclosure_viewing_walk_nodes: None ) -> None:
   gorilla_rows = EnclosureViewingWalkNodeLookup.for_species_exhibit(
      'Western Lowland Gorilla',
      AFRICAN_RAINFOREST_PAVILION )

   assert len( gorilla_rows ) == 2
   assert { row[ 'enclosure_type' ] for row in gorilla_rows } == { 'Indoor', 'Outdoor' }


def Test_ForSpeciesExhibit_TestGreaterKuduSavanna_ExpectTwoOutdoorSpots(
      stub_enclosure_viewing_walk_nodes: None ) -> None:
   kudu_rows = EnclosureViewingWalkNodeLookup.for_species_exhibit(
      'Greater Kudu',
      AFRICA_SAVANNA )

   assert len( kudu_rows ) == 2
   assert all( row[ 'enclosure_type' ] == 'Outdoor' for row in kudu_rows )
   assert len( { row[ 'walk_node_id' ] for row in kudu_rows } ) == 2


def Test_ForSpeciesExhibit_TestGreaterKuduPavilion_ExpectSingleOutdoorSpot(
      stub_enclosure_viewing_walk_nodes: None ) -> None:
   kudu_pavilion_rows = EnclosureViewingWalkNodeLookup.for_species_exhibit(
      'Greater Kudu',
      AFRICAN_RAINFOREST_PAVILION )

   assert len( kudu_pavilion_rows ) == 1
   assert kudu_pavilion_rows[ 0 ][ 'walk_node_id' ] == 'v-2003'


def Test_ForSpeciesExhibit_TestGreveysZebra_ExpectDistinctSavannaAndDomainNodes(
      stub_enclosure_viewing_walk_nodes: None ) -> None:
   zebra_savanna_rows = EnclosureViewingWalkNodeLookup.for_species_exhibit(
      "Grevy's Zebra",
      AFRICA_SAVANNA )
   zebra_domain_rows = EnclosureViewingWalkNodeLookup.for_species_exhibit(
      "Grevy's Zebra",
      CANADIAN_DOMAIN )

   assert len( zebra_savanna_rows ) == 1
   assert len( zebra_domain_rows ) == 1
   assert zebra_domain_rows[ 0 ][ 'walk_node_id' ] == 'v-3002'


def Test_ForViewingSpot_TestCoordinates_ExpectMatchingRow(
      stub_enclosure_viewing_walk_nodes: None ) -> None:
   viewing_spot = EnclosureViewingWalkNodeLookup.for_viewing_spot(
      'Western Lowland Gorilla',
      AFRICAN_RAINFOREST_PAVILION,
      10.0,
      20.0 )

   assert viewing_spot == GORILLA_INDOOR


def Test_ForSpeciesExhibit_TestUnknownSpecies_ExpectEmptyList(
      stub_enclosure_viewing_walk_nodes: None ) -> None:
   assert EnclosureViewingWalkNodeLookup.for_species_exhibit(
      'Unknown Species',
      AFRICA_SAVANNA ) == []


def Test_WalkNodeIdByEnclosureName_TestOstrichSpots_ExpectResolvedWalkNodes(
      stub_enclosure_viewing_walk_nodes: None ) -> None:
   walk_node_ids = EnclosureViewingWalkNodeLookup.walk_node_id_by_enclosure_name()

   assert walk_node_ids[
      ( 'Ostrich', AFRICA_SAVANNA, None )
   ] == 'v-4001'
   assert walk_node_ids[
      ( 'Ostrich', AFRICAN_RAINFOREST_PAVILION, 'Savanna Overlook' )
   ] == 'v-4002'


def Test_WalkNodeIdByEnclosureName_TestMissingWalkNodeMatch_ExpectSkipped(
      stub_enclosure_viewing_walk_nodes: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _clear_lookup_cache()
   stub_path = MagicMock()
   stub_path.read_text.return_value = json.dumps( [
      *ENCLOSURE_VIEWING_ROWS,
      {
         'species': 'Missing Walk Node',
         'exhibit': 'Nowhere',
         'name': None,
         'enclosure_type': 'Outdoor',
         'x_coord': 99.0,
         'y_coord': 99.0,
      },
   ] )
   monkeypatch.setattr(
      'api.walk_graph.enclosure_viewing_walk_node_lookup.Paths.ENCLOSURE_VIEWING_PATH',
      stub_path )

   walk_node_ids = EnclosureViewingWalkNodeLookup.walk_node_id_by_enclosure_name()

   assert ( 'Missing Walk Node', 'Nowhere', None ) not in walk_node_ids
   _clear_lookup_cache()
