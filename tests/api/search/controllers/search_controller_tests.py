from __future__ import annotations

from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_search_coordinator import StubSearchCoordinator
import pytest

import api.http_request_handler as server
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
from api.search.coordinators.search_coordinator import SearchCoordinator


VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026
TRANSPORTATION_ROUTE = 'summer'


def _empty_search_results() -> dict[ str, list ]:
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


def _sample_search_results() -> dict[ str, list ]:
   return {
      'animals': [
         Animal( species='African Lion', exhibit='Africa Savanna', likelihood=100 )
      ],
      'pavilions': [
         Pavilion( name='Africa Pavilion', region='Africa' )
      ],
      'restaurants': [
         Restaurant( name='Africa Restaurant', location='Africa', sub_location=None )
      ],
      'restrooms': [
         Restroom( title='Entrance Restroom' )
      ],
      'gift_shops': [
         GiftShop( name='Zootique', location='Learning & Engagement Centre' )
      ],
      'attractions': [
         Attraction( name='Conservation Carousel', free_with_admission=0 )
      ],
      'transportations': [
         Transportation( name='Zoomobile', open_time='10:00 AM', close_time='4:00 PM' )
      ],
      'transportation_stations': [
         TransportationStation(
            name='Main Zoomobile Station',
            description='Station',
            x_coord=1.0,
            y_coord=2.0 )
      ],
      'wild_encounters': [
         WildEncounter(
            name='African Rainforest',
            meeting_spot='Rainforest Pavilion',
            link='https://www.torontozoo.com/wild-encounters/african-rainforest' )
      ],
      'guardians_talks': [
         GuardiansTalk(
            name='African Lion',
            location='Africa Savanna',
            x_coord=1.0,
            y_coord=2.0 )
      ],
   }


@pytest.fixture
def stub_search_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubSearchCoordinator:
   StubSearchCoordinator.instances = []
   stub = StubSearchCoordinator( results=_sample_search_results() )
   patch_coordinator_with_stub( monkeypatch, SearchCoordinator, stub )
   return stub


def Test_Search_TestHttpRequest_ExpectAddsTypeFields(
      stub_search_coordinator: StubSearchCoordinator ) -> None:
   handler = make_handler(
      '/search',
      {
         'query': 'a',
         'includeAnimals': True,
         'includePavilions': True,
         'includeRestaurants': True,
         'includeRestrooms': True,
         'includeGiftShops': True,
         'includeAttractions': True,
         'includeTransportations': True,
         'includeTransportationStations': True,
         'includeGuardiansTalks': True,
         'includeWildEncounters': True,
         'transportationRoute': TRANSPORTATION_ROUTE,
         'month': VISIT_MONTH,
         'day': VISIT_DAY,
         'year': VISIT_YEAR,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'animals' ][ 0 ][ 'type' ] == 'animal'
   assert result[ 'pavilions' ][ 0 ][ 'type' ] == 'pavilion'
   assert result[ 'restaurants' ][ 0 ][ 'type' ] == 'restaurant'
   assert result[ 'restrooms' ][ 0 ][ 'type' ] == 'restroom'
   assert result[ 'gift_shops' ][ 0 ][ 'type' ] == 'giftShop'
   assert result[ 'attractions' ][ 0 ][ 'type' ] == 'attraction'
   assert result[ 'transportations' ][ 0 ][ 'type' ] == 'transportation'
   assert result[ 'transportation_stations' ][ 0 ][ 'type' ] == 'transportationStation'
   assert result[ 'guardians_talks' ][ 0 ][ 'type' ] == 'guardiansTalk'
   assert result[ 'wild_encounters' ][ 0 ][ 'type' ] == 'wildEncounter'
   assert stub_search_coordinator.calls == [
      (
         'search',
         {
            'query': 'a',
            'include_animals': True,
            'include_pavilions': True,
            'include_restaurants': True,
            'include_restrooms': True,
            'include_gift_shops': True,
            'include_attractions': True,
            'include_transportations': True,
            'include_transportation_stations': True,
            'include_guardians_talks': True,
            'include_wild_encounters': True,
            'month': VISIT_MONTH,
            'day': VISIT_DAY,
            'year': VISIT_YEAR,
            'temp': None,
            'include_off_display_animals': False,
            'for_itinerary': False,
            'include_closed_restaurants': False,
            'include_closed_restrooms': False,
            'include_closed_attractions': False,
            'transportation_route': TRANSPORTATION_ROUTE,
         }
      )
   ]


def Test_Search_TestHttpRequest_ExpectOmittedYearPassesThrough(
      stub_search_coordinator: StubSearchCoordinator ) -> None:
   handler = make_handler(
      '/search',
      {
         'query': 'a',
         'includeGuardiansTalks': True,
         'month': VISIT_MONTH,
         'day': VISIT_DAY,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.errors == []
   assert stub_search_coordinator.calls[ -1 ] == (
      'search',
      {
         'query': 'a',
         'include_animals': False,
         'include_pavilions': False,
         'include_restaurants': False,
         'include_restrooms': False,
         'include_gift_shops': False,
         'include_attractions': False,
         'include_transportations': False,
         'include_transportation_stations': False,
         'include_guardians_talks': True,
         'include_wild_encounters': False,
         'month': VISIT_MONTH,
         'day': VISIT_DAY,
         'year': None,
         'temp': None,
         'include_off_display_animals': False,
         'for_itinerary': False,
         'include_closed_restaurants': False,
         'include_closed_restrooms': False,
         'include_closed_attractions': False,
         'transportation_route': None,
      }
   )


def Test_Search_TestHttpRequest_ExpectOmittedYearPassesThroughForWildEncounters(
      stub_search_coordinator: StubSearchCoordinator ) -> None:
   handler = make_handler(
      '/search',
      {
         'query': 'a',
         'includeWildEncounters': True,
         'month': VISIT_MONTH,
         'day': VISIT_DAY,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.errors == []
   assert stub_search_coordinator.calls[ -1 ][ 1 ][ 'year' ] is None
   assert stub_search_coordinator.calls[ -1 ][ 1 ][ 'include_wild_encounters' ] is True


def Test_Search_TestHttpRequest_ExpectReturnsEmptyCollectionsWhenCoordinatorReturnsEmpty(
      stub_search_coordinator: StubSearchCoordinator ) -> None:
   stub_search_coordinator.results = _empty_search_results()
   handler = make_handler(
      '/search',
      {
         'query': 'a',
         'includeAnimals': False,
         'includePavilions': False,
         'includeRestaurants': False,
         'includeRestrooms': False,
         'includeGiftShops': False,
         'includeAttractions': False,
         'includeTransportationStations': False,
         'includeGuardiansTalks': False,
         'includeWildEncounters': False,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result == {
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
