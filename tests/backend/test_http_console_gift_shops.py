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
         '/set-gift-shop-closed',
         {
            'giftShop': 'Zootique',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_gift_shop_as_closed',
            {
               'gift_shop': 'Zootique',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'gift_shop': 'Zootique',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-gift-shop-closure-override',
         {
            'giftShop': 'Zootique',
            'startDate': '2026-06-20',
            'endDate': '2026-06-21',
            'message': 'Closed this weekend.'
         },
         (
            'set_gift_shop_closure_override',
            {
               'gift_shop': 'Zootique',
               'start_date': '2026-06-20',
               'end_date': '2026-06-21',
               'message': 'Closed this weekend.'
            }
         ),
         {
            'success': True,
            'gift_shop': 'Zootique',
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
      '/set-gift-shop-opening-schedule',
      {
         'giftShop': 'Zootique',
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
         'set_gift_shop_opening_schedule',
         {
            'gift_shop': 'Zootique',
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
         'gift_shop': 'Zootique',
         'scheduleStartDate': '2026-06-01',
         'scheduleEndDate': '2026-06-30'
      } )


@pytest.mark.parametrize(
   'path, expected_method',
   [
      (
         '/replace-gift-shop-opening-schedule-overlaps',
         'replace_gift_shop_opening_schedule_overlaps'
      ),
      (
         '/trim-gift-shop-opening-schedule-overlaps',
         'trim_gift_shop_opening_schedule_overlaps'
      ),
   ]
)
def test_schedule_overlap_resolution_maps_payload(
      stub_database: type[ StubZooControllers ],
      path: str,
      expected_method: str ) -> None:
   assert_schedule_overlap_resolution(
      path,
      'giftShop',
      'Zootique',
      expected_method,
      'gift_shop' )


def test_opening_schedule_overlap_failure_returns_error_type(
      stub_database: type[ StubZooControllers ] ) -> None:
   assert_opening_schedule_overlap_failure(
      '/set-gift-shop-opening-schedule',
      'giftShop',
      'Zootique' )
