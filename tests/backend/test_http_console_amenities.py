from __future__ import annotations

from typing import Any

from http_console_support import assert_console_mutation_failure, assert_console_mutation_success, assert_opening_schedule_overlap_failure, assert_schedule_overlap_resolution, assert_weekly_schedule_success
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

@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
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
         }
      ),
      (
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
         }
      ),
      (
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
         }
      ),
   ]
)
def test_weekly_schedule_maps_payload_and_success_response(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      expected_call: tuple[ str, dict[ str, Any ] ],
      response_subset: dict[ str, Any ] ) -> None:
   assert_weekly_schedule_success(
      path,
      body,
      expected_call,
      response_subset )

@pytest.mark.parametrize(
   'path, body_key, item_name, expected_method, response_key',
   [
      (
         '/replace-restaurant-opening-schedule-overlaps',
         'restaurant',
         'Africa Restaurant',
         'replace_restaurant_opening_schedule_overlaps',
         'restaurant'
      ),
      (
         '/trim-restaurant-opening-schedule-overlaps',
         'restaurant',
         'Africa Restaurant',
         'trim_restaurant_opening_schedule_overlaps',
         'restaurant'
      ),
      (
         '/replace-gift-shop-opening-schedule-overlaps',
         'giftShop',
         'Zootique',
         'replace_gift_shop_opening_schedule_overlaps',
         'gift_shop'
      ),
      (
         '/trim-gift-shop-opening-schedule-overlaps',
         'giftShop',
         'Zootique',
         'trim_gift_shop_opening_schedule_overlaps',
         'gift_shop'
      ),
      (
         '/replace-attraction-opening-schedule-overlaps',
         'attraction',
         'Conservation Carousel',
         'replace_attraction_opening_schedule_overlaps',
         'attraction'
      ),
      (
         '/trim-attraction-opening-schedule-overlaps',
         'attraction',
         'Conservation Carousel',
         'trim_attraction_opening_schedule_overlaps',
         'attraction'
      ),
   ]
)
def test_schedule_overlap_resolution_maps_payload(
      stub_database: type[ StubZooControllers ],
      path: str,
      body_key: str,
      item_name: str,
      expected_method: str,
      response_key: str ) -> None:
   assert_schedule_overlap_resolution(
      path,
      body_key,
      item_name,
      expected_method,
      response_key )

@pytest.mark.parametrize(
   'path, body_key, item_name',
   [
      (
         '/set-restaurant-opening-schedule',
         'restaurant',
         'Africa Restaurant'
      ),
      (
         '/set-gift-shop-opening-schedule',
         'giftShop',
         'Zootique'
      ),
      (
         '/set-attraction-opening-schedule',
         'attraction',
         'Conservation Carousel'
      ),
   ]
)
def test_opening_schedule_overlap_failure_returns_error_type(
      stub_database: type[ StubZooControllers ],
      path: str,
      body_key: str,
      item_name: str ) -> None:
   assert_opening_schedule_overlap_failure( path, body_key, item_name )

@pytest.mark.parametrize(
   'path, body, expected_error',
   [
      (
         '/set-restaurant-opening-schedule',
         {
            'restaurant': 'Africa Restaurant'
         },
         'Could not set opening schedule for "Africa Restaurant".'
      ),
   ]
)
def test_console_mutation_returns_error_when_database_returns_false(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      expected_error: str ) -> None:
   assert_console_mutation_failure( path, body, expected_error )

