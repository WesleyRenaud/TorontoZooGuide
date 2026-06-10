from __future__ import annotations

from http_support import ANIMAL_EXHIBIT, make_handler, response_json, StubZooControllers

import api.server as server
from api.shared.constants import itinerary_config_to_dict

def test_itinerary_endpoints_return_success_payloads(
      stub_database: type[ StubZooControllers ] ) -> None:
   set_handler = make_handler(
      '/set-itinerary',
      {
         'date': '2026-06-15',
         'arrivalTime': '09:30',
         'departureTime': '17:00',
         'animals': [],
         'attractions': [],
         'guardiansTalks': [],
         'wildEncounters': [],
         'selectedExhibits': [ ANIMAL_EXHIBIT ]
      }
   )
   get_handler = make_handler( '/get-itinerary' )
   clear_handler = make_handler( '/clear-itinerary' )
   accept_handler = make_handler( '/accept-itinerary' )

   server.MyHandler.do_POST( set_handler )
   server.MyHandler.do_POST( get_handler )
   server.MyHandler.do_POST( clear_handler )
   server.MyHandler.do_POST( accept_handler )

   set_response = response_json( set_handler )
   assert set_response[ 'status' ] == 'success'
   assert set_response[ 'reasons' ] == []
   assert StubZooControllers.instances[ 0 ].calls[ 0 ] == (
      'set_itinerary',
      {
         'date': '2026-06-15',
         'arrival_time': '09:30',
         'departure_time': '17:00',
         'animals': [],
         'attractions': [],
         'guardians_talks': [],
         'wild_encounters': [],
         'selected_exhibits': [ ANIMAL_EXHIBIT ],
         'visit_date_temp': None,
         'overriding_conflicting_guardians_talks': False,
         'confirming_short_visit': False,
         'confirming_early_admission': False,
         'confirming_guardians_talk_unschedule': False,
         'confirming_wild_encounter_unschedule': False,
      }
   )
   assert response_json( get_handler )[ 'itinerary' ][ 'date' ] == '2026-06-15'
   assert response_json( clear_handler )[ 'success' ] is True
   assert response_json( accept_handler )[ 'success' ] is True
   assert response_json( accept_handler )[ 'itinerary' ][ 'date' ] == '2026-06-15'
   assert StubZooControllers.instances[ 0 ].calls[ -2 ] == (
      'accept_itinerary',
      {
         'animals_to_keep': None,
         'attractions_to_keep': None,
      },
   )


def test_unschedule_itinerary_item_endpoint(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/unschedule-itinerary-item',
      {
         'itemType': 'animals',
         'key': 'African Lion||Africa Savanna',
      } )

   server.MyHandler.do_POST( handler )

   response = response_json( handler )
   assert response[ 'status' ] == 'success'
   assert response[ 'reasons' ] == []
   assert response[ 'itinerary' ] is not None
   assert StubZooControllers.instances[ 0 ].calls == [
      (
         'unschedule_itinerary_item',
         {
            'item_type': 'animals',
            'key': 'African Lion||Africa Savanna',
         },
      ),
   ]


def test_remove_item_from_itinerary_endpoint(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/remove-item-from-itinerary',
      {
         'itemType': 'attractions',
         'key': 'Conservation Carousel',
      } )

   server.MyHandler.do_POST( handler )

   response = response_json( handler )
   assert response[ 'status' ] == 'success'
   assert response[ 'reasons' ] == []
   assert response[ 'itinerary' ] is not None
   assert StubZooControllers.instances[ 0 ].calls == [
      (
         'remove_itinerary_item',
         {
            'item_type': 'attractions',
            'key': 'Conservation Carousel',
         },
      ),
   ]


def test_itinerary_time_endpoints_update_only_the_requested_time(
      stub_database: type[ StubZooControllers ] ) -> None:
   arrival_handler = make_handler(
      '/set-itinerary-arrival-time',
      { 'arrivalTime': '09:45' } )
   departure_handler = make_handler(
      '/set-itinerary-departure-time',
      { 'departureTime': None } )

   server.MyHandler.do_POST( arrival_handler )
   server.MyHandler.do_POST( departure_handler )

   assert response_json( arrival_handler ) == {
      'status': 'success',
      'reasons': [],
      'suppressed_warnings': [],
      'arrivalTime': '09:45',
      'itinerary_config': itinerary_config_to_dict(),
   }
   assert response_json( departure_handler ) == {
      'status': 'success',
      'reasons': [],
      'suppressed_warnings': [],
      'departureTime': None,
      'itinerary_config': itinerary_config_to_dict(),
   }
   assert StubZooControllers.instances[ 0 ].calls == [
      (
         'set_arrival_time',
         {
            'arrival_time': '09:45',
            'confirming_short_visit': False,
            'confirming_early_admission': False,
         },
      ),
      (
         'set_departure_time',
         {
            'departure_time': None,
            'confirming_short_visit': False,
         },
      ),
   ]


def test_suppress_itinerary_warning_endpoint(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/suppress-itinerary-warning',
      { 'warningType': 'arrivalDepartureTooClose' } )

   server.MyHandler.do_POST( handler )

   assert response_json( handler ) == {
      'status': 'success',
      'reasons': [],
      'suppressed_warnings': [],
      'itinerary_config': itinerary_config_to_dict(),
   }
   assert StubZooControllers.instances[ 0 ].calls == [
      (
         'suppress_itinerary_warning',
         { 'warning_type': 'arrivalDepartureTooClose' },
      ),
   ]


def test_accept_itinerary_endpoint_passes_animals_to_keep(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/accept-itinerary',
      {
         'temp': 22.5,
         'animalsToKeep': [
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
            },
         ],
      },
   )

   server.MyHandler.do_POST( handler )

   response = response_json( handler )

   assert response[ 'success' ] is True
   assert response[ 'itinerary' ][ 'date' ] == '2026-06-15'
   assert StubZooControllers.instances[ 0 ].calls[ 0 ] == (
      'accept_itinerary',
      {
         'animals_to_keep': [
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
            },
         ],
         'attractions_to_keep': None,
      },
   )
   assert StubZooControllers.instances[ 0 ].calls[ 1 ] == (
      'get_itinerary',
      { 'visit_date_temp': 22.5 },
   )


def test_accept_itinerary_endpoint_passes_attractions_to_keep(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/accept-itinerary',
      {
         'attractionsToKeep': [ 'Conservation Carousel' ],
      },
   )

   server.MyHandler.do_POST( handler )

   response = response_json( handler )

   assert response[ 'success' ] is True
   assert StubZooControllers.instances[ 0 ].calls[ 0 ] == (
      'accept_itinerary',
      {
         'animals_to_keep': None,
         'attractions_to_keep': [ 'Conservation Carousel' ],
      },
   )
