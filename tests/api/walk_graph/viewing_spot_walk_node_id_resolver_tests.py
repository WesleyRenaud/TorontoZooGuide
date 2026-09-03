from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from api.walk_graph.data_access.enclosure_viewing_walk_node_provider import EnclosureViewingWalkNodeProvider
from api.walk_graph.domain.enclosure_viewing_walk_node import EnclosureViewingWalkNode
from api.walk_graph.enclosure_viewing_walk_node_lookup import EnclosureViewingWalkNodeLookup
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver


AFRICAN_RAINFOREST_PAVILION = 'African Rainforest Pavilion'

TORTOISE_OUTDOOR: EnclosureViewingWalkNode = {
   'species': 'Aldabra Tortoise',
   'exhibit': AFRICAN_RAINFOREST_PAVILION,
   'enclosure_type': 'Outdoor',
   'x': 47.091,
   'y': 66.261,
   'walk_node_id': 'v-9001',
   'snap_distance_px': 0.0,
}

WALK_NODE_ROWS = [ TORTOISE_OUTDOOR ]

ENCLOSURE_VIEWING_ROWS = [
   {
      'species': 'Aldabra Tortoise',
      'exhibit': AFRICAN_RAINFOREST_PAVILION,
      'name': 'Outdoor',
      'enclosure_type': 'Outdoor',
      'x_coord': 47.091,
      'y_coord': 66.261,
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


def Test_Resolve_TestOutdoorEnclosureName_ExpectWalkNodeId(
      stub_enclosure_viewing_walk_nodes: None ) -> None:
   assert ViewingSpotWalkNodeIdResolver.resolve(
      'Aldabra Tortoise',
      AFRICAN_RAINFOREST_PAVILION,
      'Outdoor' ) == 'v-9001'


def Test_Resolve_TestCoordinates_ExpectWalkNodeId(
      stub_enclosure_viewing_walk_nodes: None ) -> None:
   assert ViewingSpotWalkNodeIdResolver.resolve(
      'Aldabra Tortoise',
      AFRICAN_RAINFOREST_PAVILION,
      None,
      47.091,
      66.261 ) == 'v-9001'


def Test_ResolveForCoordinates_TestMissingCoordinate_ExpectNone() -> None:
   assert ViewingSpotWalkNodeIdResolver.resolve_for_coordinates(
      'Aldabra Tortoise',
      'African Rainforest Pavilion',
      47.091,
      None ) is None


def Test_ResolveForCoordinates_TestUnknownSpot_ExpectNone(
      stub_enclosure_viewing_walk_nodes: None ) -> None:
   assert ViewingSpotWalkNodeIdResolver.resolve_for_coordinates(
      'Unknown Species',
      'Nowhere',
      0.0,
      0.0 ) is None
