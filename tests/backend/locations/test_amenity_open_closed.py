from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.restrooms.coordinators.restroom_coordinator import RestroomCoordinator
from api.types import Types
from conftest import DbControllers

def test_restaurant_schedule_controls_open_and_closed_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert RestaurantCoordinator.set_restaurant_opening_schedule(
      restaurant='Africa Restaurant',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday=False,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message='Closed for testing.'
   )

   open_only = RestaurantCoordinator.get_restaurants( day=15, month='June', year=2026, include_closed_restaurants=False )
   with_closed = RestaurantCoordinator.get_restaurants( day=15, month='June', year=2026, include_closed_restaurants=True )

   assert all( restaurant.name != 'Africa Restaurant' for restaurant in open_only )
   restaurant = next( item for item in with_closed if item.name == 'Africa Restaurant' )
   assert restaurant.is_closed is True
   assert restaurant.closed_message == 'Closed for testing.'


def test_gift_shop_schedule_controls_open_and_closed_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert GiftShopCoordinator.set_gift_shop_opening_schedule(
      gift_shop='Zootique',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday=False,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message='Closed for testing.'
   )

   open_only = GiftShopCoordinator.get_gift_shops( day=15, month='June', year=2026, include_closed_gift_shops=False )
   with_closed = GiftShopCoordinator.get_gift_shops( day=15, month='June', year=2026, include_closed_gift_shops=True )

   assert all( shop.name != 'Zootique' for shop in open_only )
   shop = next( item for item in with_closed if item.name == 'Zootique' )
   assert shop.is_closed is True
   assert shop.closed_message == 'Closed for testing.'


def test_restroom_status_controls_open_and_closed_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert RestroomCoordinator.set_restroom_as_closed(
      restroom='Entrance Restroom',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Closed for testing.'
   )

   open_only = RestroomCoordinator.get_restrooms( day=15, month='June', year=2026, include_closed_restrooms=False )
   with_closed = RestroomCoordinator.get_restrooms( day=15, month='June', year=2026, include_closed_restrooms=True )

   assert all( restroom.title != 'Entrance Restroom' for restroom in open_only )
   restroom = next( item for item in with_closed if item.title == 'Entrance Restroom' )
   assert restroom.is_closed is True
   assert restroom.closed_message == 'Closed for testing.'

   assert RestroomCoordinator.set_restroom_as_open(
      restroom='Entrance Restroom',
      start_date='2026-06-15',
      end_date=None
   )

   reopened = RestroomCoordinator.get_restrooms( day=15, month='June', year=2026, include_closed_restrooms=False )

   assert any( restroom.title == 'Entrance Restroom' for restroom in reopened )


def test_restroom_alert_controls_guest_message(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert RestroomCoordinator.set_restroom_alert(
      restroom='Entrance Restroom',
      alert_start_date='2026-06-01',
      alert_end_date='2026-06-30',
      message='Women\'s restroom is temporarily unavailable.'
   )

   restroom = next(
      item for item in RestroomCoordinator.get_restrooms( day=15, month='June', year=2026 )
      if item.title == 'Entrance Restroom'
   )

   assert restroom.has_alert is True
   assert restroom.alert_message == 'Women\'s restroom is temporarily unavailable.'

   assert RestroomCoordinator.remove_restroom_alert( restroom='Entrance Restroom' )

   restroom = next(
      item for item in RestroomCoordinator.get_restrooms( day=15, month='June', year=2026 )
      if item.title == 'Entrance Restroom'
   )

   assert restroom.has_alert is False
   assert restroom.alert_message is None


def test_setting_restroom_alert_twice_updates_existing_alert(
      db: DbControllers,
      cursor: Types.Cursor,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert RestroomCoordinator.set_restroom_alert(
      restroom='Entrance Restroom',
      alert_start_date='2026-06-01',
      alert_end_date='2026-06-30',
      message='Women\'s restroom is temporarily unavailable.'
   )
   assert RestroomCoordinator.set_restroom_alert(
      restroom='Entrance Restroom',
      alert_start_date='2026-06-15',
      alert_end_date='2026-07-15',
      message='Family restroom is temporarily unavailable.'
   )

   alert_rows = cursor.execute(
      """ SELECT
             ALERT_MESSAGE,
             ALERT_START_DATE,
             ALERT_END_DATE
          FROM RestroomAlert
          WHERE RESTROOM = ?;
      """,
      ( 'Entrance Restroom', )
   ).fetchall()
   restroom = next(
      item for item in RestroomCoordinator.get_restrooms( day=15, month='June', year=2026 )
      if item.title == 'Entrance Restroom'
   )

   assert len( alert_rows ) == 1
   assert dict( alert_rows[ 0 ] ) == {
      'ALERT_MESSAGE': 'Family restroom is temporarily unavailable.',
      'ALERT_START_DATE': '2026-06-15',
      'ALERT_END_DATE': '2026-07-15'
   }
   assert restroom.has_alert is True
   assert restroom.alert_message == 'Family restroom is temporarily unavailable.'


def test_attraction_schedule_controls_open_and_closed_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert AttractionCoordinator.set_attraction_opening_schedule(
      attraction='Conservation Carousel',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday=False,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message='Closed for testing.'
   )

   open_only = AttractionCoordinator.get_attractions( day=15, month='June', year=2026, include_closed_attractions=False )
   with_closed = AttractionCoordinator.get_attractions( day=15, month='June', year=2026, include_closed_attractions=True )

   assert all( attraction.name != 'Conservation Carousel' for attraction in open_only )
   attraction = next( item for item in with_closed if item.name == 'Conservation Carousel' )
   assert attraction.is_closed is True
   assert attraction.closed_message == 'Closed for testing.'

