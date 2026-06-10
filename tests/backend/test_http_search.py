from __future__ import annotations

from http_support import make_handler, response_json, StubZooControllers

import api.server as server

def test_search_endpoint_adds_type_fields(
      stub_database: type[ StubZooControllers ] ) -> None:
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
         'includeZoomobileStations': True,
         'includeGuardiansTalks': True,
         'includeWildEncounters': True,
         'zoomobileRoute': 'summer',
         'month': 'June',
         'day': 15,
         'year': 2026,
      }
   )

   server.MyHandler.do_POST( handler )
   result = response_json( handler )

   assert result[ 'animals' ][ 0 ][ 'type' ] == 'animal'
   assert result[ 'pavilions' ][ 0 ][ 'type' ] == 'pavilion'
   assert result[ 'restaurants' ][ 0 ][ 'type' ] == 'restaurant'
   assert result[ 'restrooms' ][ 0 ][ 'type' ] == 'restroom'
   assert result[ 'gift_shops' ][ 0 ][ 'type' ] == 'giftShop'
   assert result[ 'attractions' ][ 0 ][ 'type' ] == 'attraction'
   assert result[ 'zoomobile_stations' ][ 0 ][ 'type' ] == 'zoomobileStation'
   assert result[ 'guardians_talks' ][ 0 ][ 'type' ] == 'guardiansTalk'
   assert result[ 'wild_encounters' ][ 0 ][ 'type' ] == 'wildEncounter'
   assert (
      'get_restrooms_matching_query',
      {
         'query': 'a',
         'day': 15,
         'month': 'June',
         'year': 2026,
         'include_closed_restrooms': False
      }
   ) in StubZooControllers.instances[ 0 ].calls

   assert (
      'get_zoomobile_stations_matching_query',
      {
         'query': 'a',
         'route': 'summer',
         'day': 15,
         'month': 'June',
         'year': 2026,
      }
   ) in StubZooControllers.instances[ 0 ].calls

   assert (
      'get_guardians_talks_matching_query',
      {
         'query': 'a',
         'month': 'June',
         'day': 15,
         'year': 2026,
      }
   ) in StubZooControllers.instances[ 0 ].calls

   assert (
      'get_wild_encounters_matching_query',
      {
         'query': 'a',
         'month': 'June',
         'day': 15,
         'year': 2026,
      }
   ) in StubZooControllers.instances[ 0 ].calls


def test_get_guardians_talks_omitted_year_passes_through(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/get-guardians-talks',
      { 'month': 'June', 'day': 15 },
   )

   server.MyHandler.do_POST( handler )

   assert handler.errors == []
   assert (
      'get_guardians_talk_schedule',
      { 'month': 'June', 'day': 15, 'year': None },
   ) in StubZooControllers.instances[ 0 ].calls


def test_search_omitted_year_passes_through_when_guardians_included(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/search',
      {
         'query': 'a',
         'includeGuardiansTalks': True,
         'month': 'June',
         'day': 15,
      },
   )

   server.MyHandler.do_POST( handler )

   assert handler.errors == []
   assert (
      'get_guardians_talks_matching_query',
      {
         'query': 'a',
         'month': 'June',
         'day': 15,
         'year': None,
      },
   ) in StubZooControllers.instances[ 0 ].calls


def test_search_omitted_year_passes_through_when_wild_encounters_included(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/search',
      {
         'query': 'a',
         'includeWildEncounters': True,
         'month': 'June',
         'day': 15,
      },
   )

   server.MyHandler.do_POST( handler )

   assert handler.errors == []
   assert (
      'get_wild_encounters_matching_query',
      {
         'query': 'a',
         'month': 'June',
         'day': 15,
         'year': None,
      },
   ) in StubZooControllers.instances[ 0 ].calls


def test_search_endpoint_skips_unselected_types(
      stub_database: type[ StubZooControllers ] ) -> None:
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
         'includeZoomobileStations': False,
         'includeGuardiansTalks': False,
         'includeWildEncounters': False
      }
   )

   server.MyHandler.do_POST( handler )
   result = response_json( handler )

   assert result == {
      'animals': [],
      'pavilions': [],
      'restaurants': [],
      'restrooms': [],
      'gift_shops': [],
      'attractions': [],
      'zoomobile_stations': [],
      'wild_encounters': [],
      'guardians_talks': []
   }
   assert StubZooControllers.instances[ 0 ].calls == []
