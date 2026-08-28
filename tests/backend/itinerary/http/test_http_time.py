from __future__ import annotations

from http_support import make_handler, response_json, StubZooControllers

import api.http_request_handler as server
from api.shared.itinerary_config_builder import ItineraryConfigBuilder

EMPTY_ITINERARY_PATH = {
   'stops': [],
   'legs': [],
   'points': [],
}


def test_itinerary_time_endpoints_update_only_the_requested_time(
      stub_database: type[ StubZooControllers ] ) -> None:
   arrival_handler = make_handler(
      '/set-itinerary-arrival-time',
      { 'arrivalTime': '9:45 AM' } )
   departure_handler = make_handler(
      '/set-itinerary-departure-time',
      { 'departureTime': None } )

   server.HttpRequestHandler.do_POST( arrival_handler )
   server.HttpRequestHandler.do_POST( departure_handler )

   assert response_json( arrival_handler ) == {
      'status': 'success',
      'reasons': [],
      'suppressed_warnings': [],
      'itinerary_config': ItineraryConfigBuilder.to_dict(),
      'itinerary_path': EMPTY_ITINERARY_PATH,
      'itinerary': {
         'date': '2026-06-15',
         'arrival_time': '9:45 AM',
         'departure_time': None,
         'selected_exhibits': [],
         'animals': [],
         'attractions': [],
         'transportations': [],
         'transportation_stations': [],
         'guardians_talks': [],
         'wild_encounters': [],
         'events': [],
      },
   }
   assert response_json( departure_handler ) == {
      'status': 'success',
      'reasons': [],
      'suppressed_warnings': [],
      'itinerary_config': ItineraryConfigBuilder.to_dict(),
      'itinerary_path': EMPTY_ITINERARY_PATH,
      'itinerary': {
         'date': '2026-06-15',
         'arrival_time': None,
         'departure_time': None,
         'selected_exhibits': [],
         'animals': [],
         'attractions': [],
         'transportations': [],
         'transportation_stations': [],
         'guardians_talks': [],
         'wild_encounters': [],
         'events': [],
      },
   }
   assert StubZooControllers.instances[ 0 ].calls == [
      (
         'set_arrival_time',
         {
            'arrival_time': '9:45 AM',
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

   server.HttpRequestHandler.do_POST( handler )

   assert response_json( handler ) == {
      'status': 'success',
      'reasons': [],
      'suppressed_warnings': [],
      'itinerary_config': ItineraryConfigBuilder.to_dict(),
   }
   assert StubZooControllers.instances[ 0 ].calls == [
      (
         'suppress_itinerary_warning',
         { 'warning_type': 'arrivalDepartureTooClose' },
      ),
   ]
