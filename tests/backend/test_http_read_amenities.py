from __future__ import annotations

from typing import Any

from http_read_support import assert_read_endpoint_returns_json_key
from http_support import make_handler
from http_support import StubZooControllers
import pytest

import api.server as server


@pytest.mark.parametrize(
   'path, body, response_key',
   [
      ( '/get-restaurants', { 'month': 'June', 'day': 15, 'year': 2026 }, 'restaurants' ),
      ( '/get-restrooms', { 'month': 'June', 'day': 15, 'year': 2026 }, 'restrooms' ),
      ( '/get-gift-shops', { 'month': 'June', 'day': 15, 'year': 2026 }, 'gift_shops' ),
      ( '/get-attractions', { 'month': 'June', 'day': 15, 'year': 2026 }, 'attractions' ),
   ]
)
def test_read_amenity_endpoints_return_json_keys(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      response_key: str ) -> None:
   assert_read_endpoint_returns_json_key( path, body, response_key )


def test_get_restrooms_endpoint_maps_closed_toggle(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/get-restrooms',
      {
         'month': 'June',
         'day': 15,
         'year': 2026,
         'includeClosedRestrooms': True
      }
   )

   server.MyHandler.do_POST( handler )

   assert StubZooControllers.instances[ 0 ].calls == [
      (
         'get_restrooms',
         {
            'day': 15,
            'month': 'June',
            'year': 2026,
            'include_closed_restrooms': True
         }
      )
   ]
