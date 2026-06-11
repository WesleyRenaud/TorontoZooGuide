from __future__ import annotations

from typing import Any

from http_console_support import assert_console_mutation_failure, assert_console_mutation_success
from http_support import StubZooControllers
import pytest

@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/set-zoomobile-station-closed',
         {
            'zoomobileStation': 'Africa Zoomobile Station',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_zoomobile_station_as_closed',
            {
               'zoomobile_station': 'Africa Zoomobile Station',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'zoomobile_station': 'Africa Zoomobile Station',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-zoomobile-station-open',
         {
            'zoomobileStation': 'Africa Zoomobile Station'
         },
         (
            'set_zoomobile_station_as_open',
            {
               'zoomobile_station': 'Africa Zoomobile Station'
            }
         ),
         {
            'success': True,
            'zoomobile_station': 'Africa Zoomobile Station'
         }
      ),
      (
         '/set-drinking-fountains-closed',
         {
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_drinking_fountains_as_closed',
            {
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-drinking-fountains-open',
         {
            'startDate': '2026-07-01',
            'endDate': None
         },
         (
            'set_drinking_fountains_as_open',
            {
               'start_date': '2026-07-01',
               'end_date': None
            }
         ),
         {
            'success': True,
            'startDate': '2026-07-01',
            'endDate': None
         }
      ),
      (
         '/set-current-zoomobile-route',
         {
            'route': 'winter',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30'
         },
         (
            'set_current_zoomobile_route',
            {
               'route': 'winter',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30'
            }
         ),
         {
            'route': 'winter',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30'
         }
      ),
   ]
)
def test_console_mutation_maps_payload_and_success_response(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      expected_call: tuple[ str, dict[ str, Any ] ],
      response_subset: dict[ str, Any ] ) -> None:
   assert_console_mutation_success(
      path,
      body,
      expected_call,
      response_subset )

@pytest.mark.parametrize(
   'path, body, expected_error',
   [
      (
         '/set-current-zoomobile-route',
         {
            'route': 'winter'
         },
         'Could not set Zoomobile route to "winter".'
      ),
   ]
)
def test_console_mutation_returns_error_when_database_returns_false(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      expected_error: str ) -> None:
   assert_console_mutation_failure( path, body, expected_error )

