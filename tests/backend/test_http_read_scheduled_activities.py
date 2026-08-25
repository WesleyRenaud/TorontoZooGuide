from __future__ import annotations

from typing import Any

from http_read_support import assert_read_endpoint_returns_json_key
from http_support import make_handler
from http_support import response_json
from http_support import StubZooControllers
from http_support import WILD_ENCOUNTER_NAME
import pytest

import api.server as server


@pytest.mark.parametrize(
   'path, body, response_key',
   [
      ( '/get-transportation-route', { 'transportationRoute': 'summer', 'month': 'June', 'day': 15, 'year': 2026 }, 'route' ),
      ( '/get-guardians-talks', { 'month': 'June', 'day': 15, 'year': 2026 }, 'guardians_talks' ),
      ( '/get-wild-encounters', { 'month': 'June', 'day': 15, 'year': 2026 }, 'wild_encounters' ),
   ]
)
def test_read_scheduled_activity_endpoints_return_json_keys(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      response_key: str ) -> None:
   assert_read_endpoint_returns_json_key( path, body, response_key )


def test_get_wild_encounters_endpoint_uses_available_database_results(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/get-wild-encounters',
      { 'month': 'June', 'day': 21, 'year': 2026 } )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert StubZooControllers.instances[ 0 ].calls == [
      ( 'get_available_wild_encounters', { 'month': 'June', 'day': 21, 'year': 2026 } )
   ]
   assert [ item[ 'name' ] for item in result[ 'wild_encounters' ] ] == [
      WILD_ENCOUNTER_NAME
   ]
