from __future__ import annotations

from datetime import date

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.domain.itinerary_transportations_builder import ItineraryTransportationsBuilder
from api.search.coordinators.search_coordinator import SearchCoordinator
from conftest import DbControllers


def test_search_includes_route_duration_for_also_transportation_attractions(
      db: DbControllers,
) -> None:
   response = SearchCoordinator.search(
      query='Zoomobile',
      include_animals=False,
      include_pavilions=False,
      include_restaurants=False,
      include_restrooms=False,
      include_gift_shops=False,
      include_attractions=True,
      include_transportations=False,
      include_transportation_stations=False,
      include_guardians_talks=False,
      include_wild_encounters=False,
      month='June',
      day=15,
      year=2026,
      temp=None,
      include_off_display_animals=False,
      for_itinerary=True,
      include_closed_restaurants=False,
      include_closed_restrooms=False,
      include_closed_attractions=True,
      transportation_route=None,
   )

   zoomobile = next(
      attraction
      for attraction in response[ 'attractions' ]
      if attraction.name == 'Zoomobile'
   )

   assert zoomobile.is_also_transportation is True
   assert zoomobile.route_duration_minutes == 75


def test_build_itinerary_transportations_includes_route_duration(
      db: DbControllers,
) -> None:
   transportations = ItineraryTransportationsBuilder.build(
      [
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=None,
            start_time=None,
            end_time=None,
            legs=[],
            added_as_attraction=False,
         ),
      ],
      target_date=date( 2026, 6, 15 ),
   )

   assert len( transportations ) == 1
   assert transportations[ 0 ].route_duration_minutes == 75
