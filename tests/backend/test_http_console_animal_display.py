from __future__ import annotations

from typing import Any

from http_console_support import assert_console_mutation_failure
from http_console_support import assert_console_mutation_success
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


def test_console_mutation_returns_error_when_database_returns_false(
      stub_database: type[ StubZooControllers ] ) -> None:
   assert_console_mutation_failure(
      '/set-animal-off-display',
      {
         'species': 'African Lion',
         'exhibit': 'Africa Savanna',
         'viewingScope': 'all'
      },
      'No animal found with species "African Lion".' )
