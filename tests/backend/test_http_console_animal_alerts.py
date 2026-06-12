from __future__ import annotations

from typing import Any

from http_console_support import assert_console_mutation_success
from http_support import StubZooControllers
import pytest


@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/set-animal-viewing-alert',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'alertStartDate': '2026-06-01',
            'alertEndDate': '2026-06-30',
            'message': 'Hard to spot.'
         },
         (
            'set_animal_viewing_alert',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
               'alert_start_date': '2026-06-01',
               'alert_end_date': '2026-06-30',
               'message': 'Hard to spot.'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'alertStartDate': '2026-06-01',
            'alertEndDate': '2026-06-30',
            'message': 'Hard to spot.'
         }
      ),
      (
         '/remove-animal-viewing-alert',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna'
         },
         (
            'remove_animal_viewing_alert',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna'
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
