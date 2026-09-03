from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.scheduling.bulk.bulk_schedule_walk_order_builder import BulkScheduleWalkOrderBuilder
from api.walk_graph.domain.animal_master_route_stop_key import AnimalMasterRouteStopKey
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode
from api.walk_graph.master_route_provider import MasterRouteProvider
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver


PAVILION = 'African Rainforest Pavilion'

ENTRANCE_NODE_ID = 'n-1'
CHEETAH_NODE_ID = 'n-cheetah'
FAR_NODE_ID = 'n-far'


def _animal_record(
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None ) -> ItineraryAnimalRecord:
   return ItineraryAnimalRecord(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name,
      old_likelihood=None,
      new_likelihood=100,
   )


def _stop_key( animal: ItineraryAnimalRecord ) -> AnimalMasterRouteStopKey.Key:
   return animal.master_route_stop_key()


MARABOU_SAVANNA = _animal_record(
   species='Marabou Stork',
   exhibit='Africa Savanna',
   enclosure_name="Grevy's Zebra Enclosure",
)
HORNBILL_PAVILION = _animal_record(
   species='Southern Ground Hornbill',
   exhibit=PAVILION,
   enclosure_name='Savanna Overlook',
)
MARABOU_PAVILION = _animal_record(
   species='Marabou Stork',
   exhibit=PAVILION,
   enclosure_name='Savanna Overlook',
)
VULTURE_PAVILION = _animal_record(
   species='White-Headed Vulture',
   exhibit=PAVILION,
   enclosure_name='Savanna Overlook',
)
LION = _animal_record(
   species='African Lion',
   exhibit='Africa Savanna',
)
CHEETAH = _animal_record(
   species='Cheetah',
   exhibit='Indo-Malaya Outdoor',
)
PENGUIN = _animal_record(
   species='African Penguin',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
)


def _node( node_id: str, x_px: float, y_px: float ) -> WalkGraphNode:
   return {
      'id': node_id,
      'x': x_px / 100.0,
      'y': y_px / 100.0,
      'x_px': x_px,
      'y_px': y_px,
   }


TEST_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': ENTRANCE_NODE_ID,
   'nodes': [
      _node( ENTRANCE_NODE_ID, 0.0, 0.0 ),
      _node( CHEETAH_NODE_ID, 10.0, 0.0 ),
      _node( FAR_NODE_ID, 100.0, 0.0 ),
   ],
   'edges': [
      { 'from': ENTRANCE_NODE_ID, 'to': CHEETAH_NODE_ID, 'length_px': 10.0 },
      { 'from': ENTRANCE_NODE_ID, 'to': FAR_NODE_ID, 'length_px': 100.0 },
   ],
}

ROUTE_INDEX_BY_STOP_KEY = {
   _stop_key( MARABOU_SAVANNA ): 0,
   _stop_key( MARABOU_PAVILION ): 1,
   _stop_key( HORNBILL_PAVILION ): 2,
   _stop_key( VULTURE_PAVILION ): 3,
   _stop_key( PENGUIN ): 4,
   _stop_key( LION ): 5,
   _stop_key( CHEETAH ): 6,
}


@pytest.fixture
def stub_bulk_schedule_walk_order_dependencies(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      MasterRouteProvider,
      'route_index_by_stop_key',
      lambda: ROUTE_INDEX_BY_STOP_KEY )
   monkeypatch.setattr(
      ViewingSpotWalkNodeIdResolver,
      'resolve',
      lambda species, exhibit, enclosure_name=None: (
         CHEETAH_NODE_ID
         if species == 'Cheetah' and exhibit == 'Indo-Malaya Outdoor'
         else None ) )


def Test_RepresentativeWalkNodeId_TestClosestViewingSpot_ExpectNearestNode(
      stub_bulk_schedule_walk_order_dependencies: None ) -> None:
   assert BulkScheduleWalkOrderBuilder.representative_walk_node_id(
      TEST_GRAPH,
      ENTRANCE_NODE_ID,
      'Cheetah',
      'Indo-Malaya Outdoor' ) == CHEETAH_NODE_ID


def Test_SortAnimals_TestMixedEnclosures_ExpectMasterRouteOrder(
      stub_bulk_schedule_walk_order_dependencies: None ) -> None:
   animals = BulkScheduleWalkOrderBuilder.sort_animals(
      [
         MARABOU_SAVANNA,
         HORNBILL_PAVILION,
         MARABOU_PAVILION,
         VULTURE_PAVILION,
      ],
   )

   assert [ ( animal.species, animal.enclosure_name ) for animal in animals ] == [
      ( 'Marabou Stork', "Grevy's Zebra Enclosure" ),
      ( 'Marabou Stork', 'Savanna Overlook' ),
      ( 'Southern Ground Hornbill', 'Savanna Overlook' ),
      ( 'White-Headed Vulture', 'Savanna Overlook' ),
   ]


def Test_SortAnimals_TestCrossLoopAnimals_ExpectMasterRouteOrder(
      stub_bulk_schedule_walk_order_dependencies: None ) -> None:
   animals = BulkScheduleWalkOrderBuilder.sort_animals(
      [
         LION,
         CHEETAH,
         PENGUIN,
      ],
   )

   assert [ ( animal.species, animal.exhibit ) for animal in animals ] == [
      ( 'African Penguin', 'Africa Savanna' ),
      ( 'African Lion', 'Africa Savanna' ),
      ( 'Cheetah', 'Indo-Malaya Outdoor' ),
   ]


def Test_WalkTravelDistancePx_TestResolvedViewingSpot_ExpectShortestDistance(
      stub_bulk_schedule_walk_order_dependencies: None ) -> None:
   distance_px = BulkScheduleWalkOrderBuilder.walk_travel_distance_px(
      TEST_GRAPH,
      ENTRANCE_NODE_ID,
      'Cheetah',
      'Indo-Malaya Outdoor' )

   assert distance_px == 10.0


def Test_SortByNearestNeighbor_TestEmptyList_ExpectEmpty() -> None:
   assert BulkScheduleWalkOrderBuilder.sort_by_nearest_neighbor(
      TEST_GRAPH,
      [],
      start_node_id=ENTRANCE_NODE_ID ) == []


def Test_RepresentativeWalkNodeId_TestUnknownViewingSpot_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ViewingSpotWalkNodeIdResolver,
      'resolve',
      lambda species, exhibit, enclosure_name=None: None )

   assert BulkScheduleWalkOrderBuilder.representative_walk_node_id(
      TEST_GRAPH,
      ENTRANCE_NODE_ID,
      'Unknown Animal',
      'Nowhere' ) is None


def Test_SortByNearestNeighbor_TestCheetahAndLion_ExpectCheetahFirst(
      stub_bulk_schedule_walk_order_dependencies: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ViewingSpotWalkNodeIdResolver,
      'resolve',
      lambda species, exhibit, enclosure_name=None: (
         CHEETAH_NODE_ID
         if species == 'Cheetah' and exhibit == 'Indo-Malaya Outdoor'
         else FAR_NODE_ID
         if species == 'African Lion' and exhibit == 'Africa Savanna'
         else None ) )

   animals = BulkScheduleWalkOrderBuilder.sort_by_nearest_neighbor(
      TEST_GRAPH,
      [ LION, CHEETAH ],
      start_node_id=ENTRANCE_NODE_ID )

   assert [ ( animal.species, animal.exhibit ) for animal in animals ] == [
      ( 'Cheetah', 'Indo-Malaya Outdoor' ),
      ( 'African Lion', 'Africa Savanna' ),
   ]
