from __future__ import annotations

from typing import Any

from http_read_support import assert_read_endpoint_returns_json_key
from http_support import make_handler
from http_support import response_json
from http_support import StubZooControllers
import pytest

import api.server as server


def test_get_animals_by_exhibit_endpoint_adds_type_and_maps_payload(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/get-animals-by-exhibit',
      {
         'month': 'June',
         'year': 2026,
         'day': 15,
         'temp': 22,
         'exhibitsToInclude': [ 'Africa Savanna' ]
      }
   )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'animals' ][ 0 ][ 'type' ] == 'animal'
   assert StubZooControllers.instances[ 0 ].calls[ 0 ] == (
      'get_animals_viewable_on_day',
      {
         'day': 15,
         'month': 'June',
         'year': 2026,
         'temp': 22,
         'include_off_display_animals': False,
         'threshold': 0,
         'exhibits_to_include': [ 'Africa Savanna' ]
      }
   )


def test_get_visible_animals_endpoint_maps_payload_and_response(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/get-visible-animals',
      {
         'month': 'June',
         'year': 2026,
         'day': 15,
         'temp': 22,
         'includeOffDisplayAnimals': True
      }
   )

   server.MyHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler )[ 'animals' ][ 0 ][ 'species' ] == 'African Lion'
   assert StubZooControllers.instances[ 0 ].calls[ 0 ] == (
      'get_animals_viewable_on_day',
      {
         'day': 15,
         'month': 'June',
         'year': 2026,
         'temp': 22,
         'include_off_display_animals': True,
         'threshold': 0
      }
   )
   assert StubZooControllers.instances[ 0 ].closed is True


@pytest.mark.parametrize(
   'path, body, response_key',
   [
      ( '/get-animal-names-by-exhibit', { 'exhibit': 'Africa Savanna' }, 'animals' ),
      (
         '/get-animal-viewing-scopes',
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
         'viewingScopes'
      ),
      ( '/get-animal-information', {
         'species': 'African Lion',
         'exhibit': 'Africa Savanna',
      }, 'information' ),
   ]
)
def test_read_animal_endpoints_return_json_keys(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      response_key: str ) -> None:
   assert_read_endpoint_returns_json_key( path, body, response_key )
