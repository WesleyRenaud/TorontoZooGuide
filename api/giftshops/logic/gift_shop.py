from datetime import date
from datetime import datetime

from ... import zoo
from ...shared.enums import ScheduleStatus
from .gift_shop_context import GiftShopContext


def resolve_gift_shop_context( month, day ):
   normalized_month = zoo.ZooUtil.normalize_month( month=month )
   normalized_day = int( day )
   target_date = date(
      datetime.now().year,
      normalized_month,
      normalized_day )
   weekday = target_date.weekday()
   is_weekend_or_holiday = (
      weekday >= 5
      or zoo.ZooUtil.is_holiday( d=target_date ) )

   return GiftShopContext(
      normalized_month=normalized_month,
      normalized_day=normalized_day,
      target_date=target_date,
      weekday=weekday,
      is_weekend_or_holiday=is_weekend_or_holiday )


def calculate_gift_shop_likelihood( day_seasonal_availability_multiplier ):
   seasonal_multiplier = (
      day_seasonal_availability_multiplier
      if day_seasonal_availability_multiplier is not None
      else 1.0
   )
   likelihood = max( 0.0, min( seasonal_multiplier, 1.0 ) )

   return max( round( likelihood * 100 ), 0 )


def group_gift_shop_schedule_records_by_name( schedule_records ):
   schedule_records_by_gift_shop = {}

   for schedule_record in schedule_records:
      if schedule_record.gift_shop not in schedule_records_by_gift_shop:
         schedule_records_by_gift_shop[ schedule_record.gift_shop ] = []

      schedule_records_by_gift_shop[ schedule_record.gift_shop ].append( schedule_record )

   return schedule_records_by_gift_shop


def is_gift_shop_open_on_day( schedule_record, weekday, is_holiday ):
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
      schedule_records,
      target_date,
      weekday ):

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


def get_gift_shop_day_seasonal_availability_multiplier(
      gift_shop_record,
      context ):

   if context.is_weekend_or_holiday:
      return gift_shop_record.weekend_holiday_multiplier

   return gift_shop_record.weekday_multiplier


def build_gift_shop(
      gift_shop_record,
      schedule_records,
      context ):

   likelihood = 100
   closed_message = None
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
      gift_shop_records,
      schedule_records,
      context,
      include_closed_gift_shops,
      gift_shops_to_include=None ):

   gift_shops_to_include = gift_shops_to_include or []
   schedule_records_by_name = group_gift_shop_schedule_records_by_name( schedule_records )
   gift_shops = []

   for gift_shop_record in gift_shop_records:
      gift_shop = build_gift_shop(
         gift_shop_record=gift_shop_record,
         schedule_records=schedule_records_by_name.get( gift_shop_record.name, [] ),
         context=context )

      if (
            include_closed_gift_shops
            or not gift_shop.is_closed
            or gift_shop.name in gift_shops_to_include ):
         gift_shops.append( gift_shop )

   return gift_shops
