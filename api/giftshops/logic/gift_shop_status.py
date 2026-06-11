from __future__ import annotations

from .gift_shop_opening_schedule import GiftShopOpeningSchedule
from .gift_shop_schedule_override import GiftShopScheduleOverride
from ...shared.build_closed_opening_schedule_fields import build_closed_opening_schedule_fields
from ...shared.build_closure_override_fields import build_closure_override_fields
from ...shared.build_opening_schedule_weekday_fields import build_opening_schedule_weekday_fields
from ...types import DateInput


def build_gift_shop_closed_schedule(
      gift_shop: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> GiftShopOpeningSchedule:
   fields = build_closed_opening_schedule_fields(
      name=gift_shop,
      start_date=start_date,
      end_date=end_date,
      message=message )

   return GiftShopOpeningSchedule(
      gift_shop=gift_shop,
      start_date=fields.start_date,
      end_date=fields.end_date,
      monday=fields.monday,
      tuesday=fields.tuesday,
      wednesday=fields.wednesday,
      thursday=fields.thursday,
      friday=fields.friday,
      saturday=fields.saturday,
      sunday=fields.sunday,
      holidays_only=fields.holidays_only,
      message=fields.message )


def build_gift_shop_opening_schedule(
      gift_shop: str,
      start_date: DateInput,
      end_date: DateInput,
      monday: bool,
      tuesday: bool,
      wednesday: bool,
      thursday: bool,
      friday: bool,
      saturday: bool,
      sunday: bool,
      holidays_only: bool,
      message: str ) -> GiftShopOpeningSchedule:
   fields = build_opening_schedule_weekday_fields(
      name=gift_shop,
      start_date=start_date,
      end_date=end_date,
      monday=monday,
      tuesday=tuesday,
      wednesday=wednesday,
      thursday=thursday,
      friday=friday,
      saturday=saturday,
      sunday=sunday,
      holidays_only=holidays_only,
      message=message )

   return GiftShopOpeningSchedule(
      gift_shop=gift_shop,
      start_date=fields.start_date,
      end_date=fields.end_date,
      monday=fields.monday,
      tuesday=fields.tuesday,
      wednesday=fields.wednesday,
      thursday=fields.thursday,
      friday=fields.friday,
      saturday=fields.saturday,
      sunday=fields.sunday,
      holidays_only=fields.holidays_only,
      message=fields.message )


def build_gift_shop_closure_override(
      gift_shop: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> GiftShopScheduleOverride:
   fields = build_closure_override_fields(
      name=gift_shop,
      start_date=start_date,
      end_date=end_date,
      message=message )

   return GiftShopScheduleOverride(
      gift_shop=gift_shop,
      start_date=fields.start_date,
      end_date=fields.end_date,
      is_closed=fields.is_closed,
      message=fields.message )
