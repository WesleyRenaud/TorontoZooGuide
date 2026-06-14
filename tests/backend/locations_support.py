from __future__ import annotations

from datetime import date

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.data_access.attraction import fetch_attraction_schedule_records
from api.attractions.data_access.attraction_schedule_record import AttractionScheduleRecord
from api.attractions.logic.attraction import get_active_attraction_schedule_status
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.giftshops.data_access.gift_shop import fetch_gift_shop_schedule_records
from api.giftshops.data_access.gift_shop_schedule_record import GiftShopScheduleRecord
from api.giftshops.logic.gift_shop import get_active_gift_shop_schedule_status
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.restaurants.data_access.restaurant import fetch_restaurant_schedule_records
from api.restaurants.data_access.restaurant_schedule_record import RestaurantScheduleRecord
from api.restaurants.domain.restaurant import get_active_restaurant_schedule_status
from api.shared.enums import ScheduleStatus
from conftest import DbControllers


AmenityScheduleRecord = (
   AttractionScheduleRecord
   | GiftShopScheduleRecord
   | RestaurantScheduleRecord
)


def apply_amenity_opening_schedule(
      db: DbControllers,
      setter_name: str,
      schedule: dict[ str, object ] ) -> bool:
   if setter_name == 'set_restaurant_opening_schedule':
      return RestaurantCoordinator.set_restaurant_opening_schedule( **schedule )

   if setter_name == 'set_gift_shop_opening_schedule':
      return GiftShopCoordinator.set_gift_shop_opening_schedule( **schedule )

   if setter_name == 'set_attraction_opening_schedule':
      return AttractionCoordinator.set_attraction_opening_schedule( **schedule )

   raise AssertionError( setter_name )


def get_amenity_schedule_status(
      db: DbControllers,
      method_name: str,
      item_name: str,
      target_date: date,
      weekday: int ) -> tuple[ ScheduleStatus, str | None ]:

   if method_name == 'get_active_restaurant_schedule_status':
      return get_active_restaurant_schedule_status(
         schedule_records=[
            schedule_record
            for schedule_record in fetch_restaurant_schedule_records( db.conn )
            if schedule_record.restaurant == item_name
         ],
         target_date=target_date,
         weekday=weekday )

   if method_name == 'get_active_gift_shop_schedule_status':
      return get_active_gift_shop_schedule_status(
         schedule_records=[
            schedule_record
            for schedule_record in fetch_gift_shop_schedule_records( db.conn )
            if schedule_record.gift_shop == item_name
         ],
         target_date=target_date,
         weekday=weekday )

   return get_active_attraction_schedule_status(
      schedule_records=[
         schedule_record
         for schedule_record in fetch_attraction_schedule_records( db.conn )
         if schedule_record.attraction == item_name
      ],
      attraction_name=item_name,
      target_date=target_date,
      weekday=weekday )
