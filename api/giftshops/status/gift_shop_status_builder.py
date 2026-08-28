from __future__ import annotations

from ..scheduling.gift_shop_opening_schedule import GiftShopOpeningSchedule
from ..scheduling.gift_shop_schedule_override import GiftShopScheduleOverride
from ...shared.amenity_status_builders import AmenityStatusBuilders
from ...shared.enums import AmenityNameField
from ...types import Types


class GiftShopStatusBuilder():
   _builders = AmenityStatusBuilders(
      name_field=AmenityNameField.GIFT_SHOP,
      opening_schedule_class=GiftShopOpeningSchedule,
      schedule_override_class=GiftShopScheduleOverride,
   )


   @classmethod
   def build_closed_schedule(
         cls,
         gift_shop: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> GiftShopOpeningSchedule:
      return cls._builders.build_closed_schedule( gift_shop, start_date, end_date, message )


   @classmethod
   def build_opening_schedule(
         cls,
         gift_shop: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> GiftShopOpeningSchedule:
      return cls._builders.build_opening_schedule(
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


   @classmethod
   def build_closure_override(
         cls,
         gift_shop: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> GiftShopScheduleOverride:
      return cls._builders.build_closure_override( gift_shop, start_date, end_date, message )
