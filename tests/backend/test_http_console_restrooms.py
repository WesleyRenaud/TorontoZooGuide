from __future__ import annotations

from typing import Any

from http_console_support import assert_console_mutation_success
from http_support import StubZooControllers
import pytest

@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/set-restroom-closed',
         {
            'restroom': 'Entrance Restroom',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_restroom_as_closed',
            {
               'restroom': 'Entrance Restroom',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'restroom': 'Entrance Restroom',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-restroom-open',
         {
            'restroom': 'Entrance Restroom',
            'startDate': '2026-06-01',
            'endDate': None
         },
         (
            'set_restroom_as_open',
            {
               'restroom': 'Entrance Restroom',
               'start_date': '2026-06-01',
               'end_date': None
            }
         ),
         {
            'success': True,
            'restroom': 'Entrance Restroom',
            'startDate': '2026-06-01',
            'endDate': None
         }
      ),
      (
         '/set-restroom-alert',
         {
            'restroom': 'Entrance Restroom',
            'alertStartDate': '2026-06-01',
            'alertEndDate': '2026-06-30',
            'message': 'Women\'s restroom is temporarily unavailable.'
         },
         (
            'set_restroom_alert',
            {
               'restroom': 'Entrance Restroom',
               'alert_start_date': '2026-06-01',
               'alert_end_date': '2026-06-30',
               'message': 'Women\'s restroom is temporarily unavailable.'
            }
         ),
         {
            'success': True,
            'restroom': 'Entrance Restroom',
            'alertStartDate': '2026-06-01',
            'alertEndDate': '2026-06-30',
            'message': 'Women\'s restroom is temporarily unavailable.'
         }
      ),
      (
         '/remove-restroom-alert',
         {
            'restroom': 'Entrance Restroom'
         },
         (
            'remove_restroom_alert',
            {
               'restroom': 'Entrance Restroom'
            }
         ),
         {
            'success': True,
            'restroom': 'Entrance Restroom'
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
