from __future__ import annotations

from typing import Any

from http_console_support import assert_console_mutation_success
from http_support import StubZooControllers
import pytest


@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/create-event',
         {
            'name': 'Conservation Carousel Ride Night',
            'location': 'Front Courtyard',
            'description': 'Evening carousel rides for a special cause.',
            'link': 'https://www.torontozoo.com/events/carousel-night',
            'startDate': '2026-06-15',
            'endDate': '2026-06-30'
         },
         (
            'create_event',
            {
               'name': 'Conservation Carousel Ride Night',
               'location': 'Front Courtyard',
               'description': 'Evening carousel rides for a special cause.',
               'link': 'https://www.torontozoo.com/events/carousel-night',
               'start_date': '2026-06-15',
               'end_date': '2026-06-30'
            }
         ),
         {
            'success': True,
            'name': 'Conservation Carousel Ride Night',
            'location': 'Front Courtyard',
            'description': 'Evening carousel rides for a special cause.',
            'link': 'https://www.torontozoo.com/events/carousel-night',
            'startDate': '2026-06-15',
            'endDate': '2026-06-30'
         }
      ),
      (
         '/create-event',
         {
            'name': 'Open-ended event',
            'location': 'Front Courtyard',
            'description': 'This has no end date.',
            'link': 'https://www.torontozoo.com/events/open',
            'startDate': '2026-06-01',
            'endDate': None
         },
         (
            'create_event',
            {
               'name': 'Open-ended event',
               'location': 'Front Courtyard',
               'description': 'This has no end date.',
               'link': 'https://www.torontozoo.com/events/open',
               'start_date': '2026-06-01',
               'end_date': None
            }
         ),
         {
            'success': True,
            'name': 'Open-ended event',
            'location': 'Front Courtyard',
            'description': 'This has no end date.',
            'link': 'https://www.torontozoo.com/events/open',
            'startDate': '2026-06-01',
            'endDate': None
         }
      ),
   ]
)
def test_console_mutation_maps_payload_and_success_response(
      path: str,
      body: dict[ str, Any ],
      expected_call: tuple[ str, dict[ str, Any ] ],
      response_subset: dict[ str, Any ],
      stub_database: type[ StubZooControllers ] ) -> None:
   assert_console_mutation_success(
      path=path,
      body=body,
      expected_call=expected_call,
      response_subset=response_subset )
