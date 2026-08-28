from __future__ import annotations

from http_support import ANIMAL_EXHIBIT, make_handler, response_json, StubZooControllers

import api.http_request_handler as server
from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey


def test_itinerary_endpoints_return_success_payloads(
      stub_database: type[ StubZooControllers ] ) -> None:
   set_handler = make_handler(
      '/set-itinerary',
      {
         'date': '2026-06-15',
         'arrivalTime': '09:30',
         'departureTime': '17:00',
         'selectedExhibits': [ ANIMAL_EXHIBIT ],
         'animals': [],
         'attractions': [],
         'guardiansTalks': [],
         'wildEncounters': [],
      }
   )
   get_handler = make_handler( '/get-itinerary' )
   clear_handler = make_handler( '/clear-itinerary' )
   accept_handler = make_handler( '/accept-itinerary' )

   server.HttpRequestHandler.do_POST( set_handler )
   server.HttpRequestHandler.do_POST( get_handler )
   server.HttpRequestHandler.do_POST( clear_handler )
   server.HttpRequestHandler.do_POST( accept_handler )

   set_response = response_json( set_handler )
   assert set_response[ 'status' ] == 'success'
   assert set_response[ 'reasons' ] == []
   assert set_response[ 'itinerary_path' ] == {
      'stops': [],
      'legs': [],
      'points': [],
   }
   assert StubZooControllers.instances[ 0 ].calls[ 0 ] == (
      'set_itinerary',
      {
         'date': '2026-06-15',
         'arrival_time': '09:30',
         'departure_time': '17:00',
         'selected_exhibits': [ ANIMAL_EXHIBIT ],
         'animals': [],
         'attractions': [],
         'transportations': [],
         'guardians_talks': [],
         'wild_encounters': [],
         'visit_date_temp': None,
         'overriding_conflicting_guardians_talks': False,
         'confirming_short_visit': False,
         'confirming_early_admission': False,
         'confirming_guardians_talk_unschedule': False,
         'confirming_wild_encounter_unschedule': False,
         'confirming_fixed_time_item_long_wait': False,
         'confirming_guardians_talk_without_animal': False,
         'confirming_attraction_without_animal': False,
      }
   )
   assert response_json( get_handler )[ 'itinerary' ][ 'date' ] == '2026-06-15'
   assert response_json( get_handler )[ 'itinerary_path' ] == {
      'stops': [],
      'legs': [],
      'points': [],
   }
   assert response_json( clear_handler )[ 'success' ] is True
   assert response_json( accept_handler )[ 'success' ] is True
   assert response_json( accept_handler )[ 'itinerary' ][ 'date' ] == '2026-06-15'
   assert response_json( accept_handler )[ 'itinerary_path' ] == {
      'stops': [],
      'legs': [],
      'points': [],
   }
   assert StubZooControllers.instances[ 0 ].calls[ -2 ] == (
      'AcceptItineraryProvider.accept_itinerary',
      {
         'animals_to_keep': None,
         'attractions_to_keep': None,
      },
   )
