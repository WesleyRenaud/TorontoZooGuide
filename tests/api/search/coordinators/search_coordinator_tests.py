from __future__ import annotations

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.models.animal import Animal
from api.models.attraction import Attraction
from api.models.gift_shop import GiftShop
from api.models.guardians_talk import GuardiansTalk
from api.models.pavilion import Pavilion
from api.models.restaurant import Restaurant
from api.models.restroom import Restroom
from api.models.transportation import Transportation
from api.models.transportation_station import TransportationStation
from api.models.wild_encounter import WildEncounter
from api.pavilions.coordinators.pavilion_coordinator import PavilionCoordinator
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.restrooms.coordinators.restroom_coordinator import RestroomCoordinator
from api.search.coordinators.search_coordinator import SearchCoordinator
from api.search.transportation_attraction_route_duration_enricher import TransportationAttractionRouteDurationEnricher
from api.shared.constants import Constants
from api.transportation.coordinators.transportation_coordinator import TransportationCoordinator
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


QUERY = 'lion'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026
VISIT_TEMP = 22.0
TRANSPORTATION_ROUTE = 'summer'

ANIMAL = Animal( species='African Lion', exhibit='Africa Savanna', likelihood=100 )
PAVILION = Pavilion( name='Africa Pavilion', region='Africa' )
RESTAURANT = Restaurant(
   name='Africa Restaurant',
   location='Africa',
   sub_location=None )
RESTROOM = Restroom( title='Entrance Restroom' )
GIFT_SHOP = GiftShop( name='Zootique', location='Learning & Engagement Centre' )
ATTRACTION = Attraction( name='Conservation Carousel', free_with_admission=0 )
TRANSPORTATION = Transportation(
   name='Zoomobile',
   open_time='10:00 AM',
   close_time='4:00 PM' )
TRANSPORTATION_STATION = TransportationStation(
   name='Main Zoomobile Station',
   description='Station',
   x_coord=1.0,
   y_coord=2.0 )
GUARDIANS_TALK = GuardiansTalk(
   name='African Lion',
   location='Africa Savanna',
   x_coord=1.0,
   y_coord=2.0 )
WILD_ENCOUNTER = WildEncounter(
   name='African Rainforest',
   meeting_spot='Rainforest Pavilion',
   link='https://www.torontozoo.com/wild-encounters/african-rainforest' )


def _empty_result() -> dict[ str, list ]:
   return {
      'animals': [],
      'pavilions': [],
      'restaurants': [],
      'restrooms': [],
      'gift_shops': [],
      'attractions': [],
      'transportations': [],
      'transportation_stations': [],
      'wild_encounters': [],
      'guardians_talks': [],
   }


def _search(
      *,
      include_all: bool = True,
      for_itinerary: bool = False,
      **overrides: object ) -> dict[ str, list ]:
   kwargs = {
      'query': QUERY,
      'include_animals': include_all,
      'include_pavilions': include_all,
      'include_restaurants': include_all,
      'include_restrooms': include_all,
      'include_gift_shops': include_all,
      'include_attractions': include_all,
      'include_transportations': include_all,
      'include_transportation_stations': include_all,
      'include_guardians_talks': include_all,
      'include_wild_encounters': include_all,
      'month': VISIT_MONTH,
      'day': VISIT_DAY,
      'year': VISIT_YEAR,
      'temp': VISIT_TEMP,
      'include_off_display_animals': False,
      'for_itinerary': for_itinerary,
      'include_closed_restaurants': False,
      'include_closed_restrooms': False,
      'include_closed_attractions': False,
      'transportation_route': TRANSPORTATION_ROUTE,
   }
   kwargs.update( overrides )
   return SearchCoordinator.search( **kwargs )


def _stub_all_coordinators(
      monkeypatch: pytest.MonkeyPatch,
      *,
      return_none: bool = False ) -> dict[ str, list ]:
   calls: dict[ str, list ] = {
      'animals': [],
      'pavilions': [],
      'restaurants': [],
      'restrooms': [],
      'gift_shops': [],
      'attractions': [],
      'enrich': [],
      'transportations': [],
      'transportation_stations': [],
      'guardians_talks': [],
      'wild_encounters': [],
   }

   def animals( **kwargs: object ) -> list[ Animal ] | None:
      calls[ 'animals' ].append( kwargs )
      return None if return_none else [ ANIMAL ]

   def pavilions( **kwargs: object ) -> list[ Pavilion ] | None:
      calls[ 'pavilions' ].append( kwargs )
      return None if return_none else [ PAVILION ]

   def restaurants( **kwargs: object ) -> list[ Restaurant ] | None:
      calls[ 'restaurants' ].append( kwargs )
      return None if return_none else [ RESTAURANT ]

   def restrooms( **kwargs: object ) -> list[ Restroom ] | None:
      calls[ 'restrooms' ].append( kwargs )
      return None if return_none else [ RESTROOM ]

   def gift_shops( **kwargs: object ) -> list[ GiftShop ] | None:
      calls[ 'gift_shops' ].append( kwargs )
      return None if return_none else [ GIFT_SHOP ]

   def attractions( **kwargs: object ) -> list[ Attraction ] | None:
      calls[ 'attractions' ].append( kwargs )
      return None if return_none else [ ATTRACTION ]

   def enrich(
         attractions_arg: list[ Attraction ],
         **kwargs: object ) -> None:
      calls[ 'enrich' ].append( {
         'attractions': attractions_arg,
         **kwargs,
      } )

   def transportations( **kwargs: object ) -> list[ Transportation ] | None:
      calls[ 'transportations' ].append( kwargs )
      return None if return_none else [ TRANSPORTATION ]

   def transportation_stations(
         **kwargs: object ) -> list[ TransportationStation ] | None:
      calls[ 'transportation_stations' ].append( kwargs )
      return None if return_none else [ TRANSPORTATION_STATION ]

   def guardians_talks( **kwargs: object ) -> list[ GuardiansTalk ] | None:
      calls[ 'guardians_talks' ].append( kwargs )
      return None if return_none else [ GUARDIANS_TALK ]

   def wild_encounters( **kwargs: object ) -> list[ WildEncounter ] | None:
      calls[ 'wild_encounters' ].append( kwargs )
      return None if return_none else [ WILD_ENCOUNTER ]

   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_matching_query',
      animals )
   monkeypatch.setattr(
      PavilionCoordinator,
      'get_pavilions_matching_query',
      pavilions )
   monkeypatch.setattr(
      RestaurantCoordinator,
      'get_restaurants_matching_query',
      restaurants )
   monkeypatch.setattr(
      RestroomCoordinator,
      'get_restrooms_matching_query',
      restrooms )
   monkeypatch.setattr(
      GiftShopCoordinator,
      'get_gift_shops_matching_query',
      gift_shops )
   monkeypatch.setattr(
      AttractionCoordinator,
      'get_attractions_matching_query',
      attractions )
   monkeypatch.setattr(
      TransportationAttractionRouteDurationEnricher,
      'enrich_for_visit',
      enrich )
   monkeypatch.setattr(
      TransportationCoordinator,
      'get_transportations_matching_query',
      transportations )
   monkeypatch.setattr(
      TransportationCoordinator,
      'get_transportation_stations_matching_query',
      transportation_stations )
   monkeypatch.setattr(
      GuardiansCoordinator,
      'get_guardians_talks_matching_query',
      guardians_talks )
   monkeypatch.setattr(
      WildEncounterCoordinator,
      'get_wild_encounters_matching_query',
      wild_encounters )

   return calls


def Test_Search_TestAllIncludesFalse_ExpectEmptyListsAndNoCoordinatorCalls(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   calls = _stub_all_coordinators( monkeypatch )

   result = _search( include_all=False )

   assert result == _empty_result()
   assert calls[ 'animals' ] == []
   assert calls[ 'pavilions' ] == []
   assert calls[ 'restaurants' ] == []
   assert calls[ 'restrooms' ] == []
   assert calls[ 'gift_shops' ] == []
   assert calls[ 'attractions' ] == []
   assert calls[ 'enrich' ] == []
   assert calls[ 'transportations' ] == []
   assert calls[ 'transportation_stations' ] == []
   assert calls[ 'guardians_talks' ] == []
   assert calls[ 'wild_encounters' ] == []


def Test_Search_TestAllIncludesTrueForItinerary_ExpectListsAndItineraryThreshold(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   calls = _stub_all_coordinators( monkeypatch )

   result = _search( for_itinerary=True )

   assert result[ 'animals' ] == [ ANIMAL ]
   assert result[ 'pavilions' ] == [ PAVILION ]
   assert result[ 'restaurants' ] == [ RESTAURANT ]
   assert result[ 'restrooms' ] == [ RESTROOM ]
   assert result[ 'gift_shops' ] == [ GIFT_SHOP ]
   assert result[ 'attractions' ] == [ ATTRACTION ]
   assert result[ 'transportations' ] == [ TRANSPORTATION ]
   assert result[ 'transportation_stations' ] == [ TRANSPORTATION_STATION ]
   assert result[ 'guardians_talks' ] == [ GUARDIANS_TALK ]
   assert result[ 'wild_encounters' ] == [ WILD_ENCOUNTER ]

   assert len( calls[ 'animals' ] ) == 1
   assert calls[ 'animals' ][ 0 ][ 'threshold' ] == (
      Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD )
   assert calls[ 'animals' ][ 0 ][ 'for_itinerary' ] is True
   assert calls[ 'animals' ][ 0 ][ 'query' ] == QUERY
   assert len( calls[ 'pavilions' ] ) == 1
   assert len( calls[ 'restaurants' ] ) == 1
   assert len( calls[ 'restrooms' ] ) == 1
   assert len( calls[ 'gift_shops' ] ) == 1
   assert len( calls[ 'attractions' ] ) == 1
   assert len( calls[ 'transportations' ] ) == 1
   assert len( calls[ 'transportation_stations' ] ) == 1
   assert calls[ 'transportation_stations' ][ 0 ][ 'route' ] == TRANSPORTATION_ROUTE
   assert len( calls[ 'guardians_talks' ] ) == 1
   assert len( calls[ 'wild_encounters' ] ) == 1


def Test_Search_TestForItineraryFalse_ExpectAnimalsThresholdNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   calls = _stub_all_coordinators( monkeypatch )

   _search(
      include_all=False,
      include_animals=True,
      for_itinerary=False )

   assert len( calls[ 'animals' ] ) == 1
   assert calls[ 'animals' ][ 0 ][ 'threshold' ] is None
   assert calls[ 'animals' ][ 0 ][ 'for_itinerary' ] is False


def Test_Search_TestIncludeAttractions_ExpectEnrichForVisitCalled(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   calls = _stub_all_coordinators( monkeypatch )

   result = _search(
      include_all=False,
      include_attractions=True )

   assert result[ 'attractions' ] == [ ATTRACTION ]
   assert len( calls[ 'enrich' ] ) == 1
   assert calls[ 'enrich' ][ 0 ][ 'attractions' ] == [ ATTRACTION ]
   assert calls[ 'enrich' ][ 0 ][ 'month' ] == VISIT_MONTH
   assert calls[ 'enrich' ][ 0 ][ 'day' ] == VISIT_DAY
   assert calls[ 'enrich' ][ 0 ][ 'year' ] == VISIT_YEAR


def Test_Search_TestCoordinatorsReturnNone_ExpectEmptyLists(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _stub_all_coordinators( monkeypatch, return_none=True )

   result = _search()

   assert result == _empty_result()
