from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.scheduling.bulk.loop_schedule_unit_builder import LoopScheduleUnitBuilder
from api.itinerary.scheduling.bulk.master_route_loop_animal_grouper import MasterRouteLoopAnimalGrouper
from api.itinerary.scheduling.bulk.master_route_loop_stop_grouper import MasterRouteLoopStopGrouper
from api.walk_graph.domain.animal_master_route_stop_key import AnimalMasterRouteStopKey
from api.walk_graph.domain.attraction_route_stop import AttractionRouteStop
from api.walk_graph.domain.master_route_loop import MasterRouteLoop
from api.walk_graph.domain.master_route_loop import ONE_WAY_LOOP_TRAVERSAL
from api.walk_graph.domain.master_route_loop import TWO_WAY_LOOP_TRAVERSAL
from api.walk_graph.domain.master_route_stop_key_builder import MasterRouteStopKeyBuilder
from api.walk_graph.domain.viewing_spot_reference import ViewingSpotReference
from api.walk_graph.map_location_walk_node_lookup import MapLocationWalkNodeLookup
from api.walk_graph.master_route_provider import MasterRouteProvider
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver


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


KOOKABURRA = _animal_record(
   species='Kookaburra',
   exhibit='Australasia Pavilion',
   enclosure_name='Indoor',
)
INDO_CHEETAH = _animal_record(
   species='Cheetah',
   exhibit='Indo-Malaya Outdoor',
)
AUSTRALASIA_TIGER = _animal_record(
   species='Amur Tiger',
   exhibit='Eurasia Wilds',
)
WESTERN_GREY_KANGAROO = _animal_record(
   species='Western Grey Kangaroo',
   exhibit='Australasia Outdoor',
)
KANGAROO_WALK_THRU = ItineraryAttractionRecord(
   attraction='Kangaroo Walk-Thru',
   old_likelihood=None,
   new_likelihood=100,
)
KANGAROO_WALK_THRU_STOP_KEY = MasterRouteStopKeyBuilder.attraction( 'Kangaroo Walk-Thru' )
HIGHLAND_CATTLE = _animal_record(
   species='Highland Cattle',
   exhibit='Eurasia Wilds',
)
WEST_CAUCASIAN_TUR = _animal_record(
   species='West Caucasian Tur',
   exhibit='Eurasia Wilds',
)
AFRICA_PENGUIN = _animal_record(
   species='African Penguin',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
)
AFRICA_CHEETAH = _animal_record(
   species='Cheetah',
   exhibit='Africa Savanna',
)
UNKNOWN_ANIMAL = _animal_record(
   species='Unknown Animal',
   exhibit='Nowhere',
)

WALK_NODE_IDS = {
   ( 'Kookaburra', 'Australasia Pavilion', 'Indoor' ): 'n-kookaburra',
   ( 'Cheetah', 'Indo-Malaya Outdoor', None ): 'n-indo-cheetah',
   ( 'Amur Tiger', 'Eurasia Wilds', None ): 'n-tiger',
   ( 'Western Grey Kangaroo', 'Australasia Outdoor', None ): 'n-kangaroo',
   ( 'Highland Cattle', 'Eurasia Wilds', None ): 'n-highland',
   ( 'West Caucasian Tur', 'Eurasia Wilds', None ): 'n-tur',
   ( 'African Penguin', 'Africa Savanna', 'Outdoor' ): 'n-penguin',
   ( 'Cheetah', 'Africa Savanna', None ): 'n-africa-cheetah',
   ( 'Unknown Animal', 'Nowhere', None ): 'n-unknown',
}

LOOPS_BY_ID = {
   'australasia': MasterRouteLoop(
      loop_id='australasia',
      name='Australasia',
      traversal=ONE_WAY_LOOP_TRAVERSAL,
      viewing_spots=[
         ViewingSpotReference(
            species='Kookaburra',
            exhibit='Australasia Pavilion',
            name='Indoor' ),
         ViewingSpotReference(
            species='Western Grey Kangaroo',
            exhibit='Australasia Outdoor',
            name=None ),
         AttractionRouteStop( name='Kangaroo Walk-Thru' ),
         ViewingSpotReference(
            species='Amur Tiger',
            exhibit='Eurasia Wilds',
            name=None ),
      ] ),
   'indo_malaya': MasterRouteLoop(
      loop_id='indo_malaya',
      name='Indo-Malaya',
      traversal=ONE_WAY_LOOP_TRAVERSAL,
      viewing_spots=[
         ViewingSpotReference(
            species='Cheetah',
            exhibit='Indo-Malaya Outdoor',
            name=None ),
      ] ),
   'eurasia_wilds': MasterRouteLoop(
      loop_id='eurasia_wilds',
      name='Eurasia Wilds',
      traversal=TWO_WAY_LOOP_TRAVERSAL,
      viewing_spots=[
         ViewingSpotReference(
            species='Highland Cattle',
            exhibit='Eurasia Wilds',
            name=None ),
         ViewingSpotReference(
            species='West Caucasian Tur',
            exhibit='Eurasia Wilds',
            name=None ),
      ] ),
   'africa_savanna_canadian_domain': MasterRouteLoop(
      loop_id='africa_savanna_canadian_domain',
      name='Africa Savanna',
      traversal=ONE_WAY_LOOP_TRAVERSAL,
      viewing_spots=[
         ViewingSpotReference(
            species='African Penguin',
            exhibit='Africa Savanna',
            name='Outdoor' ),
         ViewingSpotReference(
            species='Cheetah',
            exhibit='Africa Savanna',
            name=None ),
      ] ),
}

LOOP_ID_BY_STOP_KEY = {
   _stop_key( KOOKABURRA ): 'australasia',
   _stop_key( INDO_CHEETAH ): 'indo_malaya',
   _stop_key( AUSTRALASIA_TIGER ): 'australasia',
   _stop_key( WESTERN_GREY_KANGAROO ): 'australasia',
   KANGAROO_WALK_THRU_STOP_KEY: 'australasia',
   _stop_key( HIGHLAND_CATTLE ): 'eurasia_wilds',
   _stop_key( WEST_CAUCASIAN_TUR ): 'eurasia_wilds',
   _stop_key( AFRICA_PENGUIN ): 'africa_savanna_canadian_domain',
   _stop_key( AFRICA_CHEETAH ): 'africa_savanna_canadian_domain',
}

LOOP_SIDE_CLUSTER_ID_BY_LOOP_ID = {
   'australasia': 'north',
   'indo_malaya': 'south',
   'eurasia_wilds': 'north',
   'africa_savanna_canadian_domain': 'south',
}

LOOP_INDEX_IN_SIDE_CLUSTER_BY_LOOP_ID = {
   'australasia': 0,
   'indo_malaya': 1,
   'eurasia_wilds': 2,
   'africa_savanna_canadian_domain': 3,
}

ROUTE_INDEX_BY_STOP_KEY = {
   _stop_key( KOOKABURRA ): 0,
   _stop_key( INDO_CHEETAH ): 1,
   _stop_key( AUSTRALASIA_TIGER ): 2,
   _stop_key( WESTERN_GREY_KANGAROO ): 2,
   KANGAROO_WALK_THRU_STOP_KEY: 2,
   _stop_key( HIGHLAND_CATTLE ): 3,
   _stop_key( WEST_CAUCASIAN_TUR ): 4,
   _stop_key( AFRICA_PENGUIN ): 5,
   _stop_key( AFRICA_CHEETAH ): 6,
}

LOOP_INDEX_BY_STOP_KEY = {
   _stop_key( KOOKABURRA ): 0,
   _stop_key( INDO_CHEETAH ): 1,
   _stop_key( AUSTRALASIA_TIGER ): 0,
   _stop_key( WESTERN_GREY_KANGAROO ): 0,
   KANGAROO_WALK_THRU_STOP_KEY: 0,
   _stop_key( HIGHLAND_CATTLE ): 2,
   _stop_key( WEST_CAUCASIAN_TUR ): 2,
   _stop_key( AFRICA_PENGUIN ): 3,
   _stop_key( AFRICA_CHEETAH ): 3,
}


@pytest.fixture
def stub_loop_schedule_unit_builder_dependencies(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ViewingSpotWalkNodeIdResolver,
      'resolve',
      lambda species, exhibit, enclosure_name=None: WALK_NODE_IDS.get(
         ( species, exhibit, enclosure_name ) ) )
   monkeypatch.setattr(
      MasterRouteProvider,
      'loops_by_id',
      lambda: LOOPS_BY_ID )
   monkeypatch.setattr(
      MasterRouteProvider,
      'loop_id_by_stop_key',
      lambda: LOOP_ID_BY_STOP_KEY )
   monkeypatch.setattr(
      MasterRouteProvider,
      'loop_side_cluster_id_by_loop_id',
      lambda: LOOP_SIDE_CLUSTER_ID_BY_LOOP_ID )
   monkeypatch.setattr(
      MasterRouteProvider,
      'loop_index_in_side_cluster_by_loop_id',
      lambda: LOOP_INDEX_IN_SIDE_CLUSTER_BY_LOOP_ID )
   monkeypatch.setattr(
      MasterRouteProvider,
      'route_index_by_stop_key',
      lambda: ROUTE_INDEX_BY_STOP_KEY )
   monkeypatch.setattr(
      MasterRouteProvider,
      'loop_index_by_stop_key',
      lambda: LOOP_INDEX_BY_STOP_KEY )


def Test_Build_TestGroupedAnimals_ExpectLoopMetadataAndWalkEndpoints(
      stub_loop_schedule_unit_builder_dependencies: None ) -> None:
   loop_units = LoopScheduleUnitBuilder.build(
      MasterRouteLoopAnimalGrouper.group( [ KOOKABURRA, INDO_CHEETAH ] ) )

   assert len( loop_units ) == 2

   australasia_unit = loop_units[ 0 ]
   indo_unit = loop_units[ 1 ]

   assert australasia_unit.loop_id == 'australasia'
   assert australasia_unit.side_cluster_id == 'north'
   assert australasia_unit.entry_walk_node_id == 'n-kookaburra'
   assert australasia_unit.exit_walk_node_id == 'n-kookaburra'
   assert [ animal.species for animal in australasia_unit.stops ] == [ 'Kookaburra' ]

   assert indo_unit.loop_id == 'indo_malaya'
   assert indo_unit.side_cluster_id == 'south'
   assert indo_unit.entry_walk_node_id == 'n-indo-cheetah'
   assert indo_unit.exit_walk_node_id == 'n-indo-cheetah'
   assert [ animal.species for animal in indo_unit.stops ] == [ 'Cheetah' ]


def Test_Build_TestPartialLoopAnimal_ExpectItineraryAnimalEndpoints(
      stub_loop_schedule_unit_builder_dependencies: None ) -> None:
   loop_units = LoopScheduleUnitBuilder.build(
      MasterRouteLoopAnimalGrouper.group( [ AUSTRALASIA_TIGER ] ) )

   assert len( loop_units ) == 1
   assert loop_units[ 0 ].loop_id == 'australasia'
   assert loop_units[ 0 ].entry_walk_node_id == 'n-tiger'
   assert loop_units[ 0 ].exit_walk_node_id == 'n-tiger'


def Test_Build_TestTwoWayLoop_ExpectTraversalAndEndpoints(
      stub_loop_schedule_unit_builder_dependencies: None ) -> None:
   loop_units = LoopScheduleUnitBuilder.build(
      MasterRouteLoopAnimalGrouper.group( [ HIGHLAND_CATTLE, WEST_CAUCASIAN_TUR ] ) )

   assert len( loop_units ) == 1
   assert loop_units[ 0 ].traversal == TWO_WAY_LOOP_TRAVERSAL
   assert loop_units[ 0 ].entry_walk_node_id == 'n-highland'
   assert loop_units[ 0 ].exit_walk_node_id == 'n-tur'


def Test_Reversed_TestTwoWayLoop_ExpectSwappedEndpointsAndStops(
      stub_loop_schedule_unit_builder_dependencies: None ) -> None:
   loop_units = LoopScheduleUnitBuilder.build(
      MasterRouteLoopAnimalGrouper.group( [ HIGHLAND_CATTLE, WEST_CAUCASIAN_TUR ] ) )
   reversed_unit = LoopScheduleUnitBuilder.reversed( loop_units[ 0 ] )

   assert reversed_unit.entry_walk_node_id == 'n-tur'
   assert reversed_unit.exit_walk_node_id == 'n-highland'
   assert [ animal.species for animal in reversed_unit.stops ] == [
      'West Caucasian Tur',
      'Highland Cattle',
   ]


def Test_Build_TestLoopViewingSpotOrder_ExpectSortedStops(
      stub_loop_schedule_unit_builder_dependencies: None ) -> None:
   loop_units = LoopScheduleUnitBuilder.build(
      [
         [
            AFRICA_CHEETAH,
            AFRICA_PENGUIN,
         ],
      ] )

   assert len( loop_units ) == 1
   assert loop_units[ 0 ].loop_id == 'africa_savanna_canadian_domain'
   assert [ animal.species for animal in loop_units[ 0 ].stops ] == [
      'African Penguin',
      'Cheetah',
   ]


def Test_Build_TestUnmappedAnimal_ExpectNoLoopMetadata(
      stub_loop_schedule_unit_builder_dependencies: None ) -> None:
   loop_units = LoopScheduleUnitBuilder.build( [ [ UNKNOWN_ANIMAL ] ] )

   assert len( loop_units ) == 1
   assert loop_units[ 0 ].loop_id is None
   assert loop_units[ 0 ].side_cluster_id is None


def Test_Build_TestWovenAttractionBetweenAnimals_ExpectMasterRouteOrder(
      stub_loop_schedule_unit_builder_dependencies: None ) -> None:
   stops = [
      AUSTRALASIA_TIGER,
      KANGAROO_WALK_THRU,
      WESTERN_GREY_KANGAROO,
   ]
   loop_units = LoopScheduleUnitBuilder.build(
      MasterRouteLoopStopGrouper.group( stops ) )

   australasia = next(
      unit
      for unit in loop_units
      if unit.loop_id == 'australasia' )
   ordered_names = [
      stop.attraction
      if isinstance( stop, ItineraryAttractionRecord )
      else stop.species
      for stop in australasia.stops
   ]

   assert ordered_names == [
      'Western Grey Kangaroo',
      'Kangaroo Walk-Thru',
      'Amur Tiger',
   ]


def Test_WalkNodeIdForStop_TestUnknownAttraction_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      MapLocationWalkNodeLookup,
      'for_map_location',
      lambda kind, name: None )

   assert LoopScheduleUnitBuilder.walk_node_id_for_stop(
      ItineraryAttractionRecord(
         attraction='Not A Real Attraction',
         old_likelihood=None,
         new_likelihood=100 ) ) is None
