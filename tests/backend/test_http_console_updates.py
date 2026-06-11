from __future__ import annotations

from typing import Any

from http_console_support import assert_console_mutation_success
from http_support import StubZooControllers
import pytest

@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/create-update',
         {
            'title': 'New baby giraffe',
            'description': 'Come meet the new calf.',
            'type': 'New Arrival',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30'
         },
         (
            'create_update',
            {
               'title': 'New baby giraffe',
               'description': 'Come meet the new calf.',
               'update_type': 'New Arrival',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30'
            }
         ),
         {
            'success': True,
            'title': 'New baby giraffe',
            'description': 'Come meet the new calf.',
            'type': 'New Arrival',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30'
         }
      ),
      (
         '/create-update',
         {
            'title': 'Open-ended update',
            'description': 'This has no end date.',
            'type': 'Closure',
            'startDate': '2026-06-01',
            'endDate': None
         },
         (
            'create_update',
            {
               'title': 'Open-ended update',
               'description': 'This has no end date.',
               'update_type': 'Closure',
               'start_date': '2026-06-01',
               'end_date': None
            }
         ),
         {
            'success': True,
            'title': 'Open-ended update',
            'description': 'This has no end date.',
            'type': 'Closure',
            'startDate': '2026-06-01',
            'endDate': None
         }
      ),
      (
         '/end-update',
         {
            'title': 'New baby giraffe',
            'startDate': '2026-06-01',
            'endDate': '2026-06-15'
         },
         (
            'end_update',
            {
               'title': 'New baby giraffe',
               'start_date': '2026-06-01',
               'end_date': '2026-06-15'
            }
         ),
         {
            'success': True,
            'title': 'New baby giraffe',
            'startDate': '2026-06-01',
            'endDate': '2026-06-15'
         }
      ),
      (
         '/edit-update',
         {
            'title': 'New baby giraffe',
            'startDate': '2026-06-01',
            'description': 'Updated calf details.',
            'type': 'Closure',
            'endDate': '2026-07-15'
         },
         (
            'edit_update',
            {
               'title': 'New baby giraffe',
               'start_date': '2026-06-01',
               'description': 'Updated calf details.',
               'update_type': 'Closure',
               'end_date': '2026-07-15'
            }
         ),
         {
            'success': True,
            'title': 'New baby giraffe',
            'startDate': '2026-06-01',
            'description': 'Updated calf details.',
            'type': 'Closure',
            'endDate': '2026-07-15'
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

