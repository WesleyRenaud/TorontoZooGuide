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
UNKNOWN_ANIMAL = _animal_record(
   species='Unknown Animal',
   exhibit='Nowhere',
)

ROUTE_INDEX_BY_STOP_KEY = {
   AFRICAN_PENGUIN.master_route_stop_key(): 0,
   AFRICAN_LION.master_route_stop_key(): 1,
   INDO_CHEETAH.master_route_stop_key(): 2,
   UNKNOWN_ANIMAL.master_route_stop_key(): 3,
}

LOOP_INDEX_BY_STOP_KEY = {
   AFRICAN_PENGUIN.master_route_stop_key(): 0,
   AFRICAN_LION.master_route_stop_key(): 0,
   INDO_CHEETAH.master_route_stop_key(): 1,
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
