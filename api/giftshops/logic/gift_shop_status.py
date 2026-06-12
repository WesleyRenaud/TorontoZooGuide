from __future__ import annotations

from .gift_shop_opening_schedule import GiftShopOpeningSchedule
from .gift_shop_schedule_override import GiftShopScheduleOverride
from ...shared.build_amenity_status_builders import AmenityStatusBuilders
from ...types import DateInput


_builders = AmenityStatusBuilders(
   name_field='gift_shop',
   opening_schedule_class=GiftShopOpeningSchedule,
   schedule_override_class=GiftShopScheduleOverride,
)


def build_gift_shop_closed_schedule(
      gift_shop: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> GiftShopOpeningSchedule:
   return _builders.build_closed_schedule( gift_shop, start_date, end_date, message )


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
   return _builders.build_opening_schedule(
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
      message )


def build_gift_shop_closure_override(
      gift_shop: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> GiftShopScheduleOverride:
   return _builders.build_closure_override( gift_shop, start_date, end_date, message )


__all__ = [
   'build_gift_shop_closed_schedule',
   'build_gift_shop_opening_schedule',
   'build_gift_shop_closure_override',
]
