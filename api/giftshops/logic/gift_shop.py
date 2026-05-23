from __future__ import annotations

from datetime import date

from ... import zoo
from ...shared.enums import ScheduleStatus
from ...types import MonthInput, SeasonalMultiplier, VisitDay, VisitYear
from ..data_access.gift_shop_record import GiftShopRecord
from ..data_access.gift_shop_schedule_override_record import GiftShopScheduleOverrideRecord
from ..data_access.gift_shop_schedule_record import GiftShopScheduleRecord
from .gift_shop_context import GiftShopContext


def resolve_gift_shop_context(
      day: VisitDay,
      month: MonthInput,
      year: VisitYear ) -> GiftShopContext:
   target_date = zoo.ZooUtil.visit_target_date(
      month=month,
      day=day,
      year=year )
   weekday = target_date.weekday()
   is_weekend_or_holiday = (
      weekday >= 5
      or zoo.ZooUtil.is_holiday( d=target_date ) )

   return GiftShopContext(
      normalized_month=target_date.month,
      normalized_day=target_date.day,
      target_date=target_date,
      weekday=weekday,
      is_weekend_or_holiday=is_weekend_or_holiday )


def calculate_gift_shop_likelihood(
      day_seasonal_availability_multiplier: SeasonalMultiplier ) -> int:
   seasonal_multiplier = (
      day_seasonal_availability_multiplier
      if day_seasonal_availability_multiplier is not None
      else 1.0
   )
   likelihood = max( 0.0, min( seasonal_multiplier, 1.0 ) )

   return max( round( likelihood * 100 ), 0 )


def group_gift_shop_schedule_records_by_name(
      schedule_records: list[ GiftShopScheduleRecord ] ) -> dict[ str, list[ GiftShopScheduleRecord ] ]:
   schedule_records_by_gift_shop: dict[ str, list[ GiftShopScheduleRecord ] ] = {}

   for schedule_record in schedule_records:
      if schedule_record.gift_shop not in schedule_records_by_gift_shop:
         schedule_records_by_gift_shop[ schedule_record.gift_shop ] = []

      schedule_records_by_gift_shop[ schedule_record.gift_shop ].append( schedule_record )

   return schedule_records_by_gift_shop


def group_gift_shop_schedule_override_records_by_name(
      override_records: list[ GiftShopScheduleOverrideRecord ] ) -> dict[ str, list[ GiftShopScheduleOverrideRecord ] ]:
   override_records_by_gift_shop: dict[ str, list[ GiftShopScheduleOverrideRecord ] ] = {}

   for override_record in override_records:
      if override_record.gift_shop not in override_records_by_gift_shop:
         override_records_by_gift_shop[ override_record.gift_shop ] = []

      override_records_by_gift_shop[ override_record.gift_shop ].append( override_record )

   return override_records_by_gift_shop


def is_gift_shop_open_on_day(
      schedule_record: GiftShopScheduleRecord,
      weekday: int,
      is_holiday: bool ) -> bool:
   weekday_values = [
      schedule_record.monday,
      schedule_record.tuesday,
      schedule_record.wednesday,
      schedule_record.thursday,
      schedule_record.friday,
      schedule_record.saturday,
      schedule_record.sunday,
   ]

   return (
      bool( weekday_values[ weekday ] )
      or ( is_holiday and schedule_record.holidays_only ) )


def get_active_gift_shop_schedule_status(
      schedule_records: list[ GiftShopScheduleRecord ],
      target_date: date,
      weekday: int ) -> tuple[ ScheduleStatus, str | None ]:

   if len( schedule_records ) == 0:
      return ScheduleStatus.UNKNOWN, None

   for schedule_record in schedule_records:
      is_active = zoo.ZooUtil.is_date_in_range(
         target_date=target_date,
         start_date_value=schedule_record.schedule_start_date,
         end_date_value=schedule_record.schedule_end_date )

      if not is_active:
         continue

      is_holiday = zoo.ZooUtil.is_holiday( d=target_date )

      if is_gift_shop_open_on_day(
            schedule_record=schedule_record,
            weekday=weekday,
            is_holiday=is_holiday ):
         return ScheduleStatus.OPEN, None

      return ScheduleStatus.CLOSED, schedule_record.schedule_message

   return ScheduleStatus.UNKNOWN, None


def get_active_gift_shop_schedule_override_status(
      override_records: list[ GiftShopScheduleOverrideRecord ],
      target_date: date ) -> tuple[ ScheduleStatus, str | None ]:

   for override_record in override_records:
      is_active = zoo.ZooUtil.is_date_in_range(
         target_date=target_date,
         start_date_value=override_record.override_start_date,
         end_date_value=override_record.override_end_date )

      if not is_active:
         continue

      if override_record.is_closed:
         return ScheduleStatus.CLOSED, override_record.override_message

      return ScheduleStatus.OPEN, None

   return ScheduleStatus.UNKNOWN, None


def get_gift_shop_day_seasonal_availability_multiplier(
      gift_shop_record: GiftShopRecord,
      context: GiftShopContext ) -> SeasonalMultiplier:

   if context.is_weekend_or_holiday:
      return gift_shop_record.weekend_holiday_multiplier

   return gift_shop_record.weekday_multiplier


def build_gift_shop(
      gift_shop_record: GiftShopRecord,
      schedule_records: list[ GiftShopScheduleRecord ],
      schedule_override_records: list[ GiftShopScheduleOverrideRecord ],
      context: GiftShopContext ) -> zoo.GiftShop:

   likelihood = 100
   closed_message = None
   override_status, override_message = get_active_gift_shop_schedule_override_status(
      override_records=schedule_override_records,
      target_date=context.target_date )

   if override_status == ScheduleStatus.CLOSED:
      likelihood = 0
      closed_message = override_message
      return zoo.GiftShop(
         name=gift_shop_record.name,
         location=gift_shop_record.location,
         description=gift_shop_record.description,
         x_coord=gift_shop_record.x_coord,
         y_coord=gift_shop_record.y_coord,
         is_closed=True,
         closed_message=closed_message,
         likelihood=likelihood )

   schedule_status, schedule_message = get_active_gift_shop_schedule_status(
      schedule_records=schedule_records,
      target_date=context.target_date,
      weekday=context.weekday )

   if schedule_status == ScheduleStatus.CLOSED:
      likelihood = 0
      closed_message = schedule_message
   elif schedule_status == ScheduleStatus.UNKNOWN:
      likelihood = calculate_gift_shop_likelihood(
         get_gift_shop_day_seasonal_availability_multiplier(
            gift_shop_record=gift_shop_record,
            context=context ) )

      if likelihood == 0:
         closed_message = f'The { gift_shop_record.name } is most likely not open on this day.'

   return zoo.GiftShop(
      name=gift_shop_record.name,
      location=gift_shop_record.location,
      description=gift_shop_record.description,
      x_coord=gift_shop_record.x_coord,
      y_coord=gift_shop_record.y_coord,
      is_closed=likelihood <= 0,
      closed_message=closed_message,
      likelihood=likelihood )


def build_gift_shops(
      gift_shop_records: list[ GiftShopRecord ],
      schedule_records: list[ GiftShopScheduleRecord ],
      schedule_override_records: list[ GiftShopScheduleOverrideRecord ],
      context: GiftShopContext,
      include_closed_gift_shops: bool,
      gift_shops_to_include: list[ str ] | None = None ) -> list[ zoo.GiftShop ]:

   gift_shops_to_include = gift_shops_to_include or []
   schedule_records_by_name = group_gift_shop_schedule_records_by_name( schedule_records )
   schedule_override_records_by_name = group_gift_shop_schedule_override_records_by_name(
      schedule_override_records )
   gift_shops: list[ zoo.GiftShop ] = []

   for gift_shop_record in gift_shop_records:
      gift_shop = build_gift_shop(
         gift_shop_record=gift_shop_record,
         schedule_records=schedule_records_by_name.get( gift_shop_record.name, [] ),
         schedule_override_records=schedule_override_records_by_name.get(
            gift_shop_record.name,
            [] ),
         context=context )

      if (
            include_closed_gift_shops
            or not gift_shop.is_closed
            or gift_shop.name in gift_shops_to_include ):
         gift_shops.append( gift_shop )

   return gift_shops
