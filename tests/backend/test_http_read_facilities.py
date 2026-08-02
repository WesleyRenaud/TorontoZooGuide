from __future__ import annotations

from typing import Any

from http_read_support import assert_read_endpoint_returns_json_key
from http_support import StubZooControllers
import pytest


@pytest.mark.parametrize(
   'path, body, response_key',
   [
      ( '/get-drinking-fountains', { 'month': 'June', 'day': 15, 'year': 2026 }, 'drinking_fountains' ),
      ( '/get-defibrillators', {}, 'defibrillators' ),
      ( '/get-emergency-intercoms', {}, 'emergency_intercoms' ),
      ( '/get-guest-services', {}, 'guest_services' ),
      ( '/get-picnic-sites', {}, 'picnic_sites' ),
      ( '/get-event-sites', {}, 'event_sites' ),
      ( '/get-events', { 'month': 'June', 'day': 15, 'year': 2026 }, 'events' ),
      ( '/get-updates', { 'month': 'June', 'day': 15, 'year': 2026 }, 'updates' ),
      ( '/get-zoo-hours', { 'day': 20, 'month': 'June', 'year': 2026 }, 'hours' ),
   ]
)
def test_read_facility_endpoints_return_json_keys(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      response_key: str ) -> None:
   assert_read_endpoint_returns_json_key( path, body, response_key )
