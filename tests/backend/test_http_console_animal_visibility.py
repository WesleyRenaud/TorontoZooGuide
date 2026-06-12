from __future__ import annotations

from typing import Any

from http_console_support import assert_console_mutation_success
from http_support import StubZooControllers
import pytest


@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/set-animal-visibility-schedule',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30',
            'dailyStartTime': '09:00',
            'dailyEndTime': '10:00',
            'message': 'Morning only.'
         },
         (
            'set_animal_limited_viewing_schedule',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'daily_start_time': '09:00',
               'daily_end_time': '10:00',
               'message': 'Morning only.'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30',
            'dailyStartTime': '09:00',
            'dailyEndTime': '10:00',
            'message': 'Morning only.'
         }
      ),
      (
         '/remove-animal-visibility-schedule',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'viewingScope': 'all'
         },
         (
            'remove_animal_visibility_schedule',
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
