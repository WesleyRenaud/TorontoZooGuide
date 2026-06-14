from __future__ import annotations

from datetime import date

from ..data_access.gift_shop_record import GiftShopRecord
from ..data_access.gift_shop_schedule_override_record import GiftShopScheduleOverrideRecord
from ..data_access.gift_shop_schedule_record import GiftShopScheduleRecord
from .gift_shop_context import GiftShopContext
from ...models import GiftShop
from ...shared.enums import ScheduleStatus
from ...shared.opening_schedule_seasonal_multiplier import get_day_seasonal_availability_multiplier
from ...shared.opening_schedule_status import calculate_seasonal_likelihood
from ...shared.opening_schedule_status import get_active_opening_schedule_status
from ...shared.opening_schedule_status import get_active_schedule_override_status
from ...shared.opening_schedule_status import group_records_by_name
from ...shared.opening_schedule_status import is_open_on_weekday
from ...shared.opening_schedule_status import resolve_amenity_likelihood_and_message
from ...shared.opening_schedule_visit_context import resolve_opening_schedule_visit_context
from ...types import MonthInput, SeasonalMultiplier, VisitDay, VisitYear


def resolve_gift_shop_context(
      day: VisitDay,
      month: MonthInput,
      year: VisitYear ) -> GiftShopContext:
   return resolve_opening_schedule_visit_context(
      day=day,
      month=month,
      year=year )


def calculate_gift_shop_likelihood(
      day_seasonal_availability_multiplier: SeasonalMultiplier ) -> int:
   return calculate_seasonal_likelihood( day_seasonal_availability_multiplier )


def group_gift_shop_schedule_records_by_name(
      schedule_records: list[ GiftShopScheduleRecord ] ) -> dict[ str, list[ GiftShopScheduleRecord ] ]:
   return group_records_by_name( schedule_records, lambda record: record.gift_shop )


def group_gift_shop_schedule_override_records_by_name(
      override_records: list[ GiftShopScheduleOverrideRecord ] ) -> dict[ str, list[ GiftShopScheduleOverrideRecord ] ]:
   return group_records_by_name( override_records, lambda record: record.gift_shop )


def is_gift_shop_open_on_day(
      schedule_record: GiftShopScheduleRecord,
      weekday: int,
      is_holiday: bool ) -> bool:
   return is_open_on_weekday(
      schedule_record=schedule_record,
      weekday=weekday,
      is_holiday=is_holiday )


def get_active_gift_shop_schedule_status(
      schedule_records: list[ GiftShopScheduleRecord ],
      target_date: date,
      weekday: int ) -> tuple[ ScheduleStatus, str | None ]:
   return get_active_opening_schedule_status(
      schedule_records=schedule_records,
      target_date=target_date,
      weekday=weekday )


def get_active_gift_shop_schedule_override_status(
      override_records: list[ GiftShopScheduleOverrideRecord ],
      target_date: date ) -> tuple[ ScheduleStatus, str | None ]:
   return get_active_schedule_override_status(
      override_records=override_records,
      target_date=target_date )


def get_gift_shop_day_seasonal_availability_multiplier(
      gift_shop_record: GiftShopRecord,
      context: GiftShopContext ) -> SeasonalMultiplier:
   return get_day_seasonal_availability_multiplier(
      weekday_multiplier=gift_shop_record.weekday_multiplier,
      weekend_holiday_multiplier=gift_shop_record.weekend_holiday_multiplier,
      is_weekend_or_holiday=context.is_weekend_or_holiday )


def build_gift_shop(
      gift_shop_record: GiftShopRecord,
      schedule_records: list[ GiftShopScheduleRecord ],
      schedule_override_records: list[ GiftShopScheduleOverrideRecord ],
      context: GiftShopContext ) -> GiftShop:

   likelihood, closed_message = resolve_amenity_likelihood_and_message(
      name=gift_shop_record.name,
      schedule_records=schedule_records,
      override_records=schedule_override_records,
      target_date=context.target_date,
      weekday=context.weekday,
      seasonal_multiplier=get_gift_shop_day_seasonal_availability_multiplier(
         gift_shop_record=gift_shop_record,
         context=context ) )

   return GiftShop(
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
      gift_shops_to_include: list[ str ] | None = None ) -> list[ GiftShop ]:

   gift_shops_to_include = gift_shops_to_include or []
   schedule_records_by_name = group_gift_shop_schedule_records_by_name( schedule_records )
   schedule_override_records_by_name = group_gift_shop_schedule_override_records_by_name(
      schedule_override_records )
   gift_shops: list[ GiftShop ] = []

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
