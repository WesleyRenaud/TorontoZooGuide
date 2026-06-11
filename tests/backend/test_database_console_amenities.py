from __future__ import annotations

from collections.abc import Callable
from datetime import date

from database_console_support import get_attraction
from database_console_support import get_gift_shop
from database_console_support import get_restaurant

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from conftest import DbControllers

def test_set_restaurant_closed_and_opening_schedule_changes_restaurant_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert RestaurantCoordinator.set_restaurant_as_closed( 'Africa Restaurant', '2026-06-01', '2026-06-30', '' )

   restaurant = get_restaurant( db, 'Africa Restaurant' )

   assert restaurant.is_closed is True
   assert restaurant.likelihood == 0
   assert restaurant.closed_message == 'The Africa Restaurant is temporarily closed.'
   assert all(
      item.name != 'Africa Restaurant'
      for item in RestaurantCoordinator.get_restaurants( day=15, month='June', year=2026, include_closed_restaurants=False )
   )

   assert RestaurantCoordinator.set_restaurant_opening_schedule(
      restaurant='Africa Restaurant',
      start_date='2026-06-01',
      end_date='',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=True,
      message='' )

   restaurant = get_restaurant( db, 'Africa Restaurant' )

   assert restaurant.is_closed is False
   assert restaurant.closed_message is None
   assert restaurant.likelihood == 100

def test_set_gift_shop_closed_and_opening_schedule_changes_gift_shop_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert GiftShopCoordinator.set_gift_shop_as_closed( 'Zootique', '2026-06-01', '2026-06-30', '' )

   gift_shop = get_gift_shop( db, 'Zootique' )

   assert gift_shop.is_closed is True
   assert gift_shop.likelihood == 0
   assert gift_shop.closed_message == 'The Zootique is temporarily closed.'
   assert all(
      item.name != 'Zootique'
      for item in GiftShopCoordinator.get_gift_shops( day=15, month='June', year=2026, include_closed_gift_shops=False )
   )

   assert GiftShopCoordinator.set_gift_shop_opening_schedule(
      gift_shop='Zootique',
      start_date='2026-06-01',
      end_date='',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=True,
      message='' )

   gift_shop = get_gift_shop( db, 'Zootique' )

   assert gift_shop.is_closed is False
   assert gift_shop.closed_message is None
   assert gift_shop.likelihood == 100

def test_set_attraction_closed_and_opening_schedule_changes_attraction_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AttractionCoordinator.set_attraction_as_closed( 'Conservation Carousel', '2026-06-01', '2026-06-30', '' )

   attraction = get_attraction( db, 'Conservation Carousel' )

   assert attraction.is_closed is True
   assert attraction.likelihood == 0
   assert attraction.closed_message == 'The Conservation Carousel is temporarily closed.'
   assert all(
      item.name != 'Conservation Carousel'
      for item in AttractionCoordinator.get_attractions( day=15, month='June', year=2026, include_closed_attractions=False )
   )

   assert AttractionCoordinator.set_attraction_opening_schedule(
      attraction='Conservation Carousel',
      start_date='2026-06-01',
      end_date='',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=True,
      message='' )

   attraction = get_attraction( db, 'Conservation Carousel' )

   assert attraction.is_closed is False
   assert attraction.closed_message is None
   assert attraction.likelihood == 100
