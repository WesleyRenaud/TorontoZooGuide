from ... import zoo
from ...shared.strings import SharedStrings
from .gift_shop_opening_schedule import GiftShopOpeningSchedule
from .gift_shop_schedule_override import GiftShopScheduleOverride


def build_gift_shop_closed_schedule(
      gift_shop,
      start_date,
      end_date,
      message ):
   date_range = zoo.ZooUtil.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.temporarily_closed( gift_shop )

   return GiftShopOpeningSchedule(
      gift_shop=gift_shop,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      monday=False,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message=message )


def build_gift_shop_opening_schedule(
      gift_shop,
      start_date,
      end_date,
      monday,
      tuesday,
      wednesday,
      thursday,
      friday,
      saturday,
      sunday,
      holidays_only,
      message ):
   date_range = zoo.ZooUtil.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.not_scheduled_to_be_open_today(
         gift_shop )

   return GiftShopOpeningSchedule(
      gift_shop=gift_shop,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      monday=monday,
      tuesday=tuesday,
      wednesday=wednesday,
      thursday=thursday,
      friday=friday,
      saturday=saturday,
      sunday=sunday,
      holidays_only=holidays_only,
      message=message )


def build_gift_shop_closure_override(
      gift_shop,
      start_date,
      end_date,
      message ):
   date_range = zoo.ZooUtil.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.temporarily_closed( gift_shop )

   return GiftShopScheduleOverride(
      gift_shop=gift_shop,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      is_closed=True,
      message=message )
