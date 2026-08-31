from __future__ import annotations

import pytest

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.models.attraction import Attraction


VISIT_DAY = 15
VISIT_MONTH = 'June'
VISIT_YEAR = 2026
CAROUSEL = 'Conservation Carousel'
GREENHOUSE = 'Greenhouse'


def _attraction( name: str ) -> Attraction:
   return Attraction(
      name=name,
      free_with_admission=True )


def Test_GetAttractionsForSavedItinerary_TestEmptySavedAttractions_ExpectEmpty() -> None:
   assert AttractionCoordinator.get_attractions_for_saved_itinerary(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      saved_attractions=[],
   ) == []


def Test_GetAttractionsForSavedItinerary_TestSavedAttractions_ExpectBuilderFilteredAttractions(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   attractions = [
      _attraction( GREENHOUSE ),
      _attraction( CAROUSEL ),
      _attraction( 'Tundra Air' ),
   ]
   captured: dict[ str, object ] = {}

   def get_attractions( **kwargs: object ) -> list[ Attraction ]:
      captured[ 'kwargs' ] = kwargs
      return attractions

   monkeypatch.setattr(
      AttractionCoordinator,
      'get_attractions',
      get_attractions )

   saved_attractions = [
      ItineraryAttractionRecord(
         attraction=GREENHOUSE,
         old_likelihood=None,
         new_likelihood=None ),
      ItineraryAttractionRecord(
         attraction=CAROUSEL,
         old_likelihood=None,
         new_likelihood=None ),
   ]

   result = AttractionCoordinator.get_attractions_for_saved_itinerary(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      saved_attractions=saved_attractions,
   )

   assert captured[ 'kwargs' ] == {
      'day': VISIT_DAY,
      'month': VISIT_MONTH,
      'year': VISIT_YEAR,
      'include_closed_attractions': True,
   }
   assert [ attraction.name for attraction in result ] == [ CAROUSEL, GREENHOUSE ]
