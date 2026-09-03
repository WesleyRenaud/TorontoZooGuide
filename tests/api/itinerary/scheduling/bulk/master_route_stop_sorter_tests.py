from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.scheduling.bulk.master_route_stop_sorter import MasterRouteStopSorter
from api.walk_graph.master_route_provider import MasterRouteProvider


LION = ItineraryAnimalRecord(
   species='African Lion',
   exhibit='Africa Savanna',
   old_likelihood=None,
   new_likelihood=100,
)

ROUTE_INDEX_BY_STOP_KEY = {
   LION.master_route_stop_key(): 0,
}


@pytest.fixture
def stub_master_route_indexes( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      MasterRouteProvider,
      'route_index_by_stop_key',
      lambda: ROUTE_INDEX_BY_STOP_KEY )


def Test_Sort_TestUnmappedAttractions_ExpectMappedFirstThenNameOrder(
      stub_master_route_indexes: None ) -> None:
   unmapped_b = ItineraryAttractionRecord(
      attraction='ZZZ Unmapped Attraction B',
      old_likelihood=None,
      new_likelihood=100 )
   unmapped_a = ItineraryAttractionRecord(
      attraction='AAA Unmapped Attraction A',
      old_likelihood=None,
      new_likelihood=100 )

   ordered = MasterRouteStopSorter.sort( [ unmapped_b, LION, unmapped_a ] )

   assert ordered[ 0 ].species == 'African Lion'
   assert [
      stop.attraction
      for stop in ordered[ 1: ]
   ] == [
      'AAA Unmapped Attraction A',
      'ZZZ Unmapped Attraction B',
   ]


def Test_Sort_TestEmptyStops_ExpectEmpty(
      stub_master_route_indexes: None ) -> None:
   assert MasterRouteStopSorter.sort( [] ) == []


def Test_Sort_TestUnmappedAnimal_ExpectExhibitNameOrder(
      stub_master_route_indexes: None ) -> None:
   zebra = ItineraryAnimalRecord(
      species="Grevy's Zebra",
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )

   ordered = MasterRouteStopSorter.sort( [ zebra ] )

   assert ordered == [ zebra ]
