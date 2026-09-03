from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.scheduling.bulk.master_route_loop_animal_grouper import MasterRouteLoopAnimalGrouper
from api.itinerary.scheduling.bulk.master_route_loop_stop_grouper import MasterRouteLoopStopGrouper
from api.walk_graph.master_route_provider import MasterRouteProvider


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


AFRICAN_LION = _animal_record(
   species='African Lion',
   exhibit='Africa Savanna',
)
INDO_CHEETAH = _animal_record(
   species='Cheetah',
   exhibit='Indo-Malaya Outdoor',
)
AFRICAN_PENGUIN = _animal_record(
   species='African Penguin',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
)
AFRICA_SAVANNA_CHEETAH = _animal_record(
   species='Cheetah',
   exhibit='Africa Savanna',
)
WARTHOG = _animal_record(
   species='Warthog',
   exhibit='Africa Savanna',
)
MASAI_GIRAFFE = _animal_record(
   species='Masai Giraffe',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
)
UNKNOWN_ANIMAL = _animal_record(
   species='Unknown Animal',
   exhibit='Nowhere',
)

ROUTE_INDEX_BY_STOP_KEY = {
   AFRICAN_PENGUIN.master_route_stop_key(): 0,
   AFRICAN_LION.master_route_stop_key(): 1,
   AFRICA_SAVANNA_CHEETAH.master_route_stop_key(): 2,
   WARTHOG.master_route_stop_key(): 3,
   MASAI_GIRAFFE.master_route_stop_key(): 4,
   INDO_CHEETAH.master_route_stop_key(): 5,
   UNKNOWN_ANIMAL.master_route_stop_key(): 6,
}

LOOP_INDEX_BY_STOP_KEY = {
   AFRICAN_PENGUIN.master_route_stop_key(): 0,
   AFRICAN_LION.master_route_stop_key(): 0,
   AFRICA_SAVANNA_CHEETAH.master_route_stop_key(): 0,
   WARTHOG.master_route_stop_key(): 0,
   MASAI_GIRAFFE.master_route_stop_key(): 1,
   INDO_CHEETAH.master_route_stop_key(): 2,
}


@pytest.fixture
def stub_master_route_loop_stop_grouper( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      MasterRouteProvider,
      'route_index_by_stop_key',
      lambda: ROUTE_INDEX_BY_STOP_KEY )
   monkeypatch.setattr(
      MasterRouteProvider,
      'loop_index_by_stop_key',
      lambda: LOOP_INDEX_BY_STOP_KEY )


def Test_Group_TestMixedLoopAndUnmappedAnimals_ExpectSortedLoopGroups(
      stub_master_route_loop_stop_grouper: None ) -> None:
   animals = [
      AFRICAN_LION,
      INDO_CHEETAH,
      AFRICAN_PENGUIN,
      UNKNOWN_ANIMAL,
   ]

   groups = MasterRouteLoopStopGrouper.group( animals )

   assert len( groups ) == 3
   assert [ animal.species for animal in groups[ 0 ] ] == [
      'African Penguin',
      'African Lion',
   ]
   assert [ animal.species for animal in groups[ 1 ] ] == [ 'Cheetah' ]
   assert [ animal.species for animal in groups[ 2 ] ] == [ 'Unknown Animal' ]


def Test_Group_TestWarthogBeforeGiraffe_ExpectSeparateLoopGroupsInRouteOrder(
      stub_master_route_loop_stop_grouper: None ) -> None:
   animals = [
      MASAI_GIRAFFE,
      WARTHOG,
   ]

   groups = MasterRouteLoopStopGrouper.group( animals )

   assert len( groups ) == 2
   assert [ animal.species for animal in groups[ 0 ] ] == [ 'Warthog' ]
   assert [ animal.species for animal in groups[ 1 ] ] == [ 'Masai Giraffe' ]


def Test_Group_TestSavannaLoopAnimals_ExpectSingleLoopGroup(
      stub_master_route_loop_stop_grouper: None ) -> None:
   animals = [
      AFRICAN_LION,
      AFRICA_SAVANNA_CHEETAH,
      AFRICAN_PENGUIN,
   ]

   groups = MasterRouteLoopStopGrouper.group( animals )

   assert len( groups ) == 1
   assert [ animal.species for animal in groups[ 0 ] ] == [
      'African Penguin',
      'African Lion',
      'Cheetah',
   ]


def Test_Group_TestAnimalGrouperDelegate_ExpectSameGroups(
      stub_master_route_loop_stop_grouper: None ) -> None:
   animals = [
      AFRICAN_LION,
      INDO_CHEETAH,
      AFRICAN_PENGUIN,
      UNKNOWN_ANIMAL,
   ]

   assert MasterRouteLoopAnimalGrouper.group( animals ) == MasterRouteLoopStopGrouper.group(
      animals )


def Test_Group_TestEmptyStops_ExpectEmpty() -> None:
   assert MasterRouteLoopStopGrouper.group( [] ) == []
