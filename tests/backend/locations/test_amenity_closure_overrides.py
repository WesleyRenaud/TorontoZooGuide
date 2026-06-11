from __future__ import annotations

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.data_access.attraction import fetch_attraction_schedule_override_records
from api.attractions.data_access.attraction import fetch_attraction_schedule_records
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.giftshops.data_access.gift_shop import fetch_gift_shop_schedule_override_records
from api.giftshops.data_access.gift_shop import fetch_gift_shop_schedule_records
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.restaurants.data_access.restaurant import fetch_restaurant_schedule_override_records
from api.restaurants.data_access.restaurant import fetch_restaurant_schedule_records
from conftest import DbControllers

def test_attraction_closure_override_takes_precedence_over_opening_schedule( db: DbControllers ) -> None:
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
      message='Open for June.'
   )

   assert AttractionCoordinator.set_attraction_closure_override(
      attraction='Conservation Carousel',
      start_date='2026-06-20',
      end_date='2026-06-21',
      message='Closed this weekend.'
   )

   override_records = fetch_attraction_schedule_override_records( db.conn )
   assert [
      (
         record.attraction,
         record.override_start_date,
         record.override_end_date,
         record.is_closed,
         record.override_message
      )
      for record in override_records
      if record.attraction == 'Conservation Carousel'
   ] == [
      (
         'Conservation Carousel',
         '2026-06-20',
         '2026-06-21',
         1,
         'Closed this weekend.'
      )
   ]

   closed_attraction = next(
      attraction for attraction in AttractionCoordinator.get_attractions(
         day=20,
         month='June',
         year=2026,
         include_closed_attractions=True )
      if attraction.name == 'Conservation Carousel'
   )
   open_attraction = next(
      attraction for attraction in AttractionCoordinator.get_attractions(
         day=22,
         month='June',
         year=2026,
         include_closed_attractions=True )
      if attraction.name == 'Conservation Carousel'
   )

   assert closed_attraction.is_closed is True
   assert closed_attraction.closed_message == 'Closed this weekend.'
   assert open_attraction.is_closed is False


def test_restaurant_closure_override_takes_precedence_over_opening_schedule( db: DbControllers ) -> None:
   assert RestaurantCoordinator.set_restaurant_opening_schedule(
      restaurant='Africa Restaurant',
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
      message='Open for June.'
   )

   assert RestaurantCoordinator.set_restaurant_closure_override(
      restaurant='Africa Restaurant',
      start_date='2026-06-20',
      end_date='2026-06-21',
      message='Closed this weekend.'
   )

   override_records = fetch_restaurant_schedule_override_records( db.conn )
   assert [
      (
         record.restaurant,
         record.override_start_date,
         record.override_end_date,
         record.is_closed,
         record.override_message
      )
      for record in override_records
      if record.restaurant == 'Africa Restaurant'
   ] == [
      (
         'Africa Restaurant',
         '2026-06-20',
         '2026-06-21',
         1,
         'Closed this weekend.'
      )
   ]

   closed_restaurant = next(
      restaurant for restaurant in RestaurantCoordinator.get_restaurants(
         day=20,
         month='June',
         year=2026,
         include_closed_restaurants=True )
      if restaurant.name == 'Africa Restaurant'
   )
   open_restaurant = next(
      restaurant for restaurant in RestaurantCoordinator.get_restaurants(
         day=22,
         month='June',
         year=2026,
         include_closed_restaurants=True )
      if restaurant.name == 'Africa Restaurant'
   )

   assert closed_restaurant.is_closed is True
   assert closed_restaurant.closed_message == 'Closed this weekend.'
   assert open_restaurant.is_closed is False


def test_gift_shop_closure_override_takes_precedence_over_opening_schedule( db: DbControllers ) -> None:
   assert GiftShopCoordinator.set_gift_shop_opening_schedule(
      gift_shop='Zootique',
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
      message='Open for June.'
   )

   assert GiftShopCoordinator.set_gift_shop_closure_override(
      gift_shop='Zootique',
      start_date='2026-06-20',
      end_date='2026-06-21',
      message='Closed this weekend.'
   )

   override_records = fetch_gift_shop_schedule_override_records( db.conn )
   assert [
      (
         record.gift_shop,
         record.override_start_date,
         record.override_end_date,
         record.is_closed,
         record.override_message
      )
      for record in override_records
      if record.gift_shop == 'Zootique'
   ] == [
      (
         'Zootique',
         '2026-06-20',
         '2026-06-21',
         1,
         'Closed this weekend.'
      )
   ]

   closed_gift_shop = next(
      gift_shop for gift_shop in GiftShopCoordinator.get_gift_shops(
         day=20,
         month='June',
         year=2026,
         include_closed_gift_shops=True )
      if gift_shop.name == 'Zootique'
   )
   open_gift_shop = next(
      gift_shop for gift_shop in GiftShopCoordinator.get_gift_shops(
         day=22,
         month='June',
         year=2026,
         include_closed_gift_shops=True )
      if gift_shop.name == 'Zootique'
   )

   assert closed_gift_shop.is_closed is True
   assert closed_gift_shop.closed_message == 'Closed this weekend.'
   assert open_gift_shop.is_closed is False


