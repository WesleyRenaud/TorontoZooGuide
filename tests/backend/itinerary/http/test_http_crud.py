from __future__ import annotations

from http_support import ANIMAL_EXHIBIT, make_handler, response_json, StubZooControllers

import api.server as server


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
