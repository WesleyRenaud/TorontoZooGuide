from __future__ import annotations

from typing import Any

from http_console_support import assert_console_mutation_success
from http_console_support import assert_opening_schedule_overlap_failure
from http_console_support import assert_schedule_overlap_resolution
from http_console_support import assert_weekly_schedule_success
from http_support import StubZooControllers
import pytest


@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/set-attraction-closed',
         {
            'attraction': 'Conservation Carousel',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_attraction_as_closed',
            {
               'attraction': 'Conservation Carousel',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'attraction': 'Conservation Carousel',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-attraction-closure-override',
         {
            'attraction': 'Conservation Carousel',
            'startDate': '2026-06-20',
            'endDate': '2026-06-21',
            'message': 'Closed this weekend.'
         },
         (
            'set_attraction_closure_override',
            {
               'attraction': 'Conservation Carousel',
               'start_date': '2026-06-20',
               'end_date': '2026-06-21',
               'message': 'Closed this weekend.'
            }
         ),
         {
            'success': True,
            'attraction': 'Conservation Carousel',
            'startDate': '2026-06-20',
            'endDate': '2026-06-21',
            'message': 'Closed this weekend.'
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


def test_weekly_schedule_maps_payload_and_success_response(
      stub_database: type[ StubZooControllers ] ) -> None:
   assert_weekly_schedule_success(
      '/set-attraction-opening-schedule',
      {
         'attraction': 'Conservation Carousel',
         'scheduleStartDate': '2026-06-01',
         'scheduleEndDate': '2026-06-30',
         'monday': True,
         'tuesday': False,
         'wednesday': True,
         'thursday': False,
         'friday': True,
         'saturday': False,
         'sunday': True,
         'holidaysOnly': False,
         'message': 'Schedule.'
      },
      (
         'set_attraction_opening_schedule',
         {
            'attraction': 'Conservation Carousel',
            'start_date': '2026-06-01',
            'end_date': '2026-06-30',
            'monday': True,
            'tuesday': False,
            'wednesday': True,
            'thursday': False,
            'friday': True,
            'saturday': False,
            'sunday': True,
            'holidays_only': False,
            'message': 'Schedule.'
         }
      ),
      {
         'attraction': 'Conservation Carousel',
         'scheduleStartDate': '2026-06-01',
         'scheduleEndDate': '2026-06-30'
      } )


@pytest.mark.parametrize(
   'path, expected_method',
   [
      (
         '/replace-attraction-opening-schedule-overlaps',
         'replace_attraction_opening_schedule_overlaps'
      ),
      (
         '/trim-attraction-opening-schedule-overlaps',
         'trim_attraction_opening_schedule_overlaps'
      ),
   ]
)
def test_schedule_overlap_resolution_maps_payload(
      stub_database: type[ StubZooControllers ],
      path: str,
      expected_method: str ) -> None:
   assert_schedule_overlap_resolution(
      path,
      'attraction',
      'Conservation Carousel',
      expected_method,
      'attraction' )


def test_opening_schedule_overlap_failure_returns_error_type(
      stub_database: type[ StubZooControllers ] ) -> None:
   assert_opening_schedule_overlap_failure(
      '/set-attraction-opening-schedule',
      'attraction',
      'Conservation Carousel' )
