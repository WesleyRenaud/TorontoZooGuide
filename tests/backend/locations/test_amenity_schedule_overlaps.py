from __future__ import annotations

from locations_support import apply_amenity_opening_schedule
import pytest

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.data_access.attraction import fetch_attraction_schedule_records
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.giftshops.data_access.gift_shop_provider import GiftShopProvider
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.restaurants.data_access.restaurant_provider import RestaurantProvider
from conftest import DbControllers

def test_attraction_opening_schedule_rejects_overlapping_date_ranges( db: DbControllers ) -> None:
   assert AttractionCoordinator.set_attraction_opening_schedule(
      attraction='Conservation Carousel',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=False,
      message='June schedule.'
   )

   assert AttractionCoordinator.set_attraction_opening_schedule(
      attraction='Conservation Carousel',
      start_date='2026-06-15',
      end_date='2026-07-15',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=False,
      message='Overlapping schedule.'
   ) is False

   assert AttractionCoordinator.set_attraction_opening_schedule(
      attraction='Conservation Carousel',
      start_date='2026-07-01',
      end_date='2026-07-31',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=False,
      message='July schedule.'
   )


@pytest.mark.parametrize(
   'setter, item_kw, item_name',
   [
      (
         RestaurantCoordinator.set_restaurant_opening_schedule,
         'restaurant',
         'Africa Restaurant'
      ),
      (
         GiftShopCoordinator.set_gift_shop_opening_schedule,
         'gift_shop',
         'Zootique'
      )
   ]
)
def test_restaurant_and_gift_shop_opening_schedules_reject_overlapping_date_ranges(
      db: DbControllers,
      setter: Callable[ ..., bool ],
      item_kw: str,
      item_name: str ) -> None:
   june_schedule = {
      item_kw: item_name,
      'start_date': '2026-06-01',
      'end_date': '2026-06-30',
      'monday': True,
      'tuesday': True,
      'wednesday': True,
      'thursday': True,
      'friday': True,
      'saturday': True,
      'sunday': True,
      'holidays_only': False,
      'message': 'June schedule.'
   }
   overlapping_schedule = {
      **june_schedule,
      'start_date': '2026-06-15',
      'end_date': '2026-07-15',
      'message': 'Overlapping schedule.'
   }
   july_schedule = {
      **june_schedule,
      'start_date': '2026-07-01',
      'end_date': '2026-07-31',
      'message': 'July schedule.'
   }

   assert setter( **june_schedule )
   assert setter( **overlapping_schedule ) is False
   assert setter( **july_schedule )


@pytest.mark.parametrize(
   'controller, item_kw, item_name, records_fetcher, record_name_attr',
   [
      (
         RestaurantCoordinator,
         'restaurant',
         'Africa Restaurant',
         RestaurantProvider.fetch_restaurant_schedule_records,
         'restaurant'
      ),
      (
         GiftShopCoordinator,
         'gift_shop',
         'Zootique',
         GiftShopProvider.fetch_gift_shop_schedule_records,
         'gift_shop'
      ),
      (
         AttractionCoordinator,
         'attraction',
         'Conservation Carousel',
         fetch_attraction_schedule_records,
         'attraction'
      )
   ]
)
def test_opening_schedule_can_replace_overlapping_schedules(
      db: DbControllers,
      controller: type,
      item_kw: str,
      item_name: str,
      records_fetcher: Callable[ [ Connection ], list[ AmenityScheduleRecord ] ],
      record_name_attr: str ) -> None:
   base_schedule = {
      item_kw: item_name,
      'start_date': '2026-06-01',
      'end_date': '2026-06-30',
      'monday': True,
      'tuesday': True,
      'wednesday': True,
      'thursday': True,
      'friday': True,
      'saturday': True,
      'sunday': True,
      'holidays_only': False,
      'message': 'June schedule.'
   }
   replacement_schedule = {
      **base_schedule,
      'start_date': '2026-06-15',
      'end_date': '2026-07-15',
      'message': 'Replacement schedule.'
   }

   set_method = getattr( controller, f'set_{ item_kw }_opening_schedule' )
   replace_method = getattr(
      controller,
      f'replace_{ item_kw }_opening_schedule_overlaps' )

   assert set_method( **base_schedule )
   assert replace_method(
      **replacement_schedule )

   schedule_records = [
      schedule_record
      for schedule_record in records_fetcher( db.conn )
      if getattr( schedule_record, record_name_attr ) == item_name
   ]

   assert [
      (
         record.schedule_start_date,
         record.schedule_end_date,
         record.schedule_message
      )
      for record in schedule_records
   ] == [
      (
         '2026-06-15',
         '2026-07-15',
         'Replacement schedule.'
      )
   ]


@pytest.mark.parametrize(
   'controller, item_kw, item_name, records_fetcher, record_name_attr',
   [
      (
         RestaurantCoordinator,
         'restaurant',
         'Africa Restaurant',
         RestaurantProvider.fetch_restaurant_schedule_records,
         'restaurant'
      ),
      (
         GiftShopCoordinator,
         'gift_shop',
         'Zootique',
         GiftShopProvider.fetch_gift_shop_schedule_records,
         'gift_shop'
      ),
      (
         AttractionCoordinator,
         'attraction',
         'Conservation Carousel',
         fetch_attraction_schedule_records,
         'attraction'
      )
   ]
)
def test_opening_schedule_can_trim_existing_schedule_around_new_schedule(
      db: DbControllers,
      controller: type,
      item_kw: str,
      item_name: str,
      records_fetcher: Callable[ [ Connection ], list[ AmenityScheduleRecord ] ],
      record_name_attr: str ) -> None:
   base_schedule = {
      item_kw: item_name,
      'start_date': '2026-06-01',
      'end_date': '2026-07-31',
      'monday': True,
      'tuesday': True,
      'wednesday': True,
      'thursday': True,
      'friday': True,
      'saturday': True,
      'sunday': True,
      'holidays_only': False,
      'message': 'Summer schedule.'
   }
   inserted_schedule = {
      **base_schedule,
      'start_date': '2026-06-15',
      'end_date': '2026-06-20',
      'message': 'Special schedule.'
   }

   set_method = getattr( controller, f'set_{ item_kw }_opening_schedule' )
   trim_method = getattr(
      controller,
      f'trim_{ item_kw }_opening_schedule_overlaps' )

   assert set_method( **base_schedule )
   assert trim_method(
      **inserted_schedule )

   schedule_records = sorted(
      [
         schedule_record
         for schedule_record in records_fetcher( db.conn )
         if getattr( schedule_record, record_name_attr ) == item_name
      ],
      key=lambda record: record.schedule_start_date )

   assert [
      (
         record.schedule_start_date,
         record.schedule_end_date,
         record.schedule_message
      )
      for record in schedule_records
   ] == [
      (
         '2026-06-01',
         '2026-06-14',
         'Summer schedule.'
      ),
      (
         '2026-06-15',
         '2026-06-20',
         'Special schedule.'
      ),
      (
         '2026-06-21',
         '2026-07-31',
         'Summer schedule.'
      )
   ]


