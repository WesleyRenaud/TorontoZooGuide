from __future__ import annotations

from typing import Any

from http_console_support import assert_console_mutation_failure
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
         '/set-restaurant-closed',
         {
            'restaurant': 'Africa Restaurant',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_restaurant_as_closed',
            {
               'restaurant': 'Africa Restaurant',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'restaurant': 'Africa Restaurant',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-restaurant-closure-override',
         {
            'restaurant': 'Africa Restaurant',
            'startDate': '2026-06-20',
            'endDate': '2026-06-21',
            'message': 'Closed this weekend.'
         },
         (
            'set_restaurant_closure_override',
            {
               'restaurant': 'Africa Restaurant',
               'start_date': '2026-06-20',
               'end_date': '2026-06-21',
               'message': 'Closed this weekend.'
            }
         ),
         {
            'success': True,
            'restaurant': 'Africa Restaurant',
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
      '/set-restaurant-opening-schedule',
      {
         'restaurant': 'Africa Restaurant',
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
         'set_restaurant_opening_schedule',
         {
            'restaurant': 'Africa Restaurant',
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
         'restaurant': 'Africa Restaurant',
         'scheduleStartDate': '2026-06-01',
         'scheduleEndDate': '2026-06-30'
      } )


@pytest.mark.parametrize(
   'path, expected_method',
   [
      (
         '/replace-restaurant-opening-schedule-overlaps',
         'replace_restaurant_opening_schedule_overlaps'
      ),
      (
         '/trim-restaurant-opening-schedule-overlaps',
         'trim_restaurant_opening_schedule_overlaps'
      ),
   ]
)
def test_schedule_overlap_resolution_maps_payload(
      stub_database: type[ StubZooControllers ],
      path: str,
      expected_method: str ) -> None:
   assert_schedule_overlap_resolution(
      path,
      'restaurant',
      'Africa Restaurant',
      expected_method,
      'restaurant' )


def test_opening_schedule_overlap_failure_returns_error_type(
      stub_database: type[ StubZooControllers ] ) -> None:
   assert_opening_schedule_overlap_failure(
      '/set-restaurant-opening-schedule',
      'restaurant',
      'Africa Restaurant' )


def test_console_mutation_returns_error_when_database_returns_false(
      stub_database: type[ StubZooControllers ] ) -> None:
   assert_console_mutation_failure(
      '/set-restaurant-opening-schedule',
      {
         'restaurant': 'Africa Restaurant'
      },
      'Could not set opening schedule for "Africa Restaurant".' )
