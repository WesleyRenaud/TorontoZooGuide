from __future__ import annotations

from typing import Any

from http_console_support import assert_console_mutation_failure, assert_console_mutation_success
from http_support import StubZooControllers
import pytest

from api.shared.enums import AnimalViewingScope

@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/set-animal-off-display',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'viewingScope': 'indoor',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Unavailable.'
         },
         (
            'set_animal_as_off_display',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
               'viewing_scope': AnimalViewingScope.INDOOR,
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Unavailable.'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'viewingScope': 'indoor',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Unavailable.'
         }
      ),
      (
         '/set-animal-on-display',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'viewingScope': 'outdoor'
         },
         (
            'set_animal_as_on_display',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
               'viewing_scope': AnimalViewingScope.OUTDOOR
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'viewingScope': 'outdoor'
         }
      ),
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
      (
         '/set-exhibit-closed',
         {
            'exhibit': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_exhibit_as_closed',
            {
               'exhibit': 'Africa Savanna',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'exhibit': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-exhibit-open',
         {
            'exhibit': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': None
         },
         (
            'set_exhibit_as_open',
            {
               'exhibit': 'Africa Savanna',
               'start_date': '2026-06-01',
               'end_date': None
            }
         ),
         {
            'success': True,
            'exhibit': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': None
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
            '/set-animal-off-display',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
               'viewingScope': 'all'
            },
            'No animal found with species "African Lion".'
         ),
      (
         '/set-exhibit-closed',
         {
            'exhibit': 'Africa Savanna'
         },
         'Could not set "Africa Savanna" as closed.'
      ),
   ]
)
def test_console_mutation_returns_error_when_database_returns_false(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      expected_error: str ) -> None:
   assert_console_mutation_failure( path, body, expected_error )

