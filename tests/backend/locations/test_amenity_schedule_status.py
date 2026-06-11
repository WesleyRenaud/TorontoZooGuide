from __future__ import annotations

from datetime import date

from locations_support import AmenityScheduleRecord, apply_amenity_opening_schedule, get_amenity_schedule_status
import pytest

from conftest import DbControllers

@pytest.mark.parametrize(
   'method_name, setter_name, item_kw, item_name',
   [
      (
         'get_active_restaurant_schedule_status',
         'set_restaurant_opening_schedule',
         'restaurant',
         'Africa Restaurant'
      ),
      (
         'get_active_gift_shop_schedule_status',
         'set_gift_shop_opening_schedule',
         'gift_shop',
         'Zootique'
      ),
      (
         'get_active_attraction_schedule_status',
         'set_attraction_opening_schedule',
         'attraction',
         'Conservation Carousel'
      )
   ]
)
@pytest.mark.parametrize(
   'target_date, weekday_flag',
   [
      ( date( 2026, 6, 15 ), 'monday' ),
      ( date( 2026, 6, 16 ), 'tuesday' ),
      ( date( 2026, 6, 17 ), 'wednesday' ),
      ( date( 2026, 6, 18 ), 'thursday' ),
      ( date( 2026, 6, 19 ), 'friday' ),
      ( date( 2026, 6, 20 ), 'saturday' ),
      ( date( 2026, 6, 21 ), 'sunday' )
   ]
)
def test_amenity_schedule_status_opens_on_each_weekday(
      db: DbControllers,
      method_name: str,
      setter_name: str,
      item_kw: str,
      item_name: str,
      target_date: date,
      weekday_flag: str ) -> None:
   schedule = {
      item_kw: item_name,
      'start_date': '2026-06-01',
      'end_date': '2026-06-30',
      'monday': False,
      'tuesday': False,
      'wednesday': False,
      'thursday': False,
      'friday': False,
      'saturday': False,
      'sunday': False,
      'holidays_only': False,
      'message': 'Closed for testing.'
   }
   schedule[ weekday_flag ] = True

   assert apply_amenity_opening_schedule( db, setter_name, schedule )

   assert get_amenity_schedule_status(
      db,
      method_name,
      item_name,
      target_date,
      target_date.weekday() ) == ( 'open', None )


@pytest.mark.parametrize(
   'method_name, setter_name, item_kw, item_name',
   [
      (
         'get_active_restaurant_schedule_status',
         'set_restaurant_opening_schedule',
         'restaurant',
         'Africa Restaurant'
      ),
      (
         'get_active_gift_shop_schedule_status',
         'set_gift_shop_opening_schedule',
         'gift_shop',
         'Zootique'
      ),
      (
         'get_active_attraction_schedule_status',
         'set_attraction_opening_schedule',
         'attraction',
         'Conservation Carousel'
      )
   ]
)
def test_amenity_schedule_status_handles_unknown_inactive_closed_and_holiday(
      db: DbControllers,
      method_name: str,
      setter_name: str,
      item_kw: str,
      item_name: str ) -> None:
   assert get_amenity_schedule_status(
      db,
      method_name,
      item_name,
      date( 2026, 5, 15 ),
      4 ) == ( 'unknown', None )

   schedule = {
      item_kw: item_name,
      'start_date': '2026-06-01',
      'end_date': '2026-06-30',
      'monday': False,
      'tuesday': False,
      'wednesday': False,
      'thursday': False,
      'friday': False,
      'saturday': False,
      'sunday': False,
      'holidays_only': False,
      'message': 'Closed for testing.'
   }

   assert apply_amenity_opening_schedule( db, setter_name, schedule )

   assert get_amenity_schedule_status(
      db,
      method_name,
      item_name,
      date( 2026, 5, 15 ),
      4 ) == ( 'unknown', None )
   assert get_amenity_schedule_status(
      db,
      method_name,
      item_name,
      date( 2026, 6, 15 ),
      0 ) == ( 'closed', 'Closed for testing.' )

   schedule[ 'end_date' ] = '2026-12-31'
   schedule[ 'holidays_only' ] = True
   assert apply_amenity_opening_schedule( db, setter_name, schedule )

   assert get_amenity_schedule_status(
      db,
      method_name,
      item_name,
      date( 2026, 12, 25 ),
      4 ) == ( 'open', None )

