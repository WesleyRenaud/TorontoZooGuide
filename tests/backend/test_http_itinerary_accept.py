from __future__ import annotations

from http_support import make_handler, response_json, StubZooControllers

import api.server as server


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
