from __future__ import annotations

from http_support import make_handler, response_json, StubZooControllers

import api.server as server
from api.shared.constants import itinerary_config_to_dict


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
