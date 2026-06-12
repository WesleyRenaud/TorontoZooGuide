from __future__ import annotations

from typing import Any

from http_read_support import assert_read_endpoint_returns_json_key
from http_support import StubZooControllers
import pytest


@pytest.mark.parametrize(
   'path, body, response_key',
   [
      ( '/get-exhibits-in-region', { 'region': 'Africa' }, 'exhibits' ),
      ( '/get-regions', {}, 'regions' ),
      ( '/get-pavilions', {}, 'pavilions' ),
      ( '/get-closed-exhibits', { 'month': 'June', 'day': 15, 'year': 2026 }, 'closed_exhibits' ),
   ]
)
def test_read_exhibit_endpoints_return_json_keys(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      response_key: str ) -> None:
   assert_read_endpoint_returns_json_key( path, body, response_key )
