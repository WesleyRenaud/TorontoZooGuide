from __future__ import annotations

from datetime import date

from locations_support import apply_amenity_opening_schedule, get_amenity_schedule_status
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
def test_amenity_schedule_status_opens_on_monday(
      db: DbControllers,
      method_name: str,
      setter_name: str,
      item_kw: str,
      item_name: str ) -> None:
   target_date = date( 2026, 6, 15 )
   schedule = {
      item_kw: item_name,
      'start_date': '2026-06-01',
      'end_date': '2026-06-30',
      'monday': True,
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
      target_date,
      target_date.weekday() ) == ( 'open', None )
