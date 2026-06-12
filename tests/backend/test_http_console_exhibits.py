from __future__ import annotations

from typing import Any

from http_console_support import assert_console_mutation_failure
from http_console_support import assert_console_mutation_success
from http_support import StubZooControllers
import pytest


@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
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


def test_console_mutation_returns_error_when_database_returns_false(
      stub_database: type[ StubZooControllers ] ) -> None:
   assert_console_mutation_failure(
      '/set-exhibit-closed',
      {
         'exhibit': 'Africa Savanna'
      },
      'Could not set "Africa Savanna" as closed.' )
