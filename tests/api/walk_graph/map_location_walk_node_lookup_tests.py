from __future__ import annotations

import pytest

from api.walk_graph.data_access.map_location_walk_node_provider import MapLocationWalkNodeProvider
from api.walk_graph.domain.map_location_kind import MapLocationKind
from api.walk_graph.domain.map_location_walk_node import MapLocationWalkNode
from api.walk_graph.map_location_walk_node_lookup import MapLocationWalkNodeLookup


KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'
PENGUIN_MEETING_SPOT = 'Wild Encounter - Penguin Meeting Spot'

PENGUIN_ROW = MapLocationWalkNode(
   kind=MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT,
   name=PENGUIN_MEETING_SPOT,
   location='',
   x=10.0,
   y=20.0,
   walk_node_id='v-5001',
   snap_distance_px=0.0,
)

KANGAROO_ROW = MapLocationWalkNode(
   kind=MapLocationKind.ATTRACTION,
   name=KANGAROO_WALK_THRU,
   location='',
   x=30.0,
   y=40.0,
   walk_node_id='v-5002',
   snap_distance_px=0.0,
)

MAP_LOCATION_ROWS = [ PENGUIN_ROW, KANGAROO_ROW ]


def _clear_lookup_cache() -> None:
   MapLocationWalkNodeLookup.by_key.cache_clear()


@pytest.fixture
def stub_map_location_walk_nodes( monkeypatch: pytest.MonkeyPatch ) -> None:
   _clear_lookup_cache()
   monkeypatch.setattr(
      MapLocationWalkNodeProvider,
      'fetch_records',
      lambda: MAP_LOCATION_ROWS )
   yield
   _clear_lookup_cache()


def Test_ForMapLocation_TestPenguinMeetingSpot_ExpectWalkNode(
      stub_map_location_walk_nodes: None ) -> None:
   row = MapLocationWalkNodeLookup.for_map_location(
      MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT,
      PENGUIN_MEETING_SPOT )

   assert row == PENGUIN_ROW


def Test_ForMapLocation_TestKangarooWalkThru_ExpectMatchingRow(
      stub_map_location_walk_nodes: None ) -> None:
   row = MapLocationWalkNodeLookup.for_map_location(
      MapLocationKind.ATTRACTION,
      KANGAROO_WALK_THRU )

   assert row == KANGAROO_ROW


def Test_ForMapLocation_TestUnknownLocation_ExpectNone(
      stub_map_location_walk_nodes: None ) -> None:
   assert MapLocationWalkNodeLookup.for_map_location(
      MapLocationKind.ATTRACTION,
      'Unknown Attraction' ) is None
