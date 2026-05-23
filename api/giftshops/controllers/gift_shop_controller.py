from __future__ import annotations

from ..data_access.gift_shop import fetch_gift_shop_names
from ..data_access.gift_shop import fetch_gift_shop_records
from ..data_access.gift_shop import fetch_gift_shop_schedule_override_records
from ..data_access.gift_shop import fetch_gift_shop_schedule_records
from ..data_access.gift_shop_schedule import save_gift_shop_opening_schedule
from ..data_access.gift_shop_schedule import save_gift_shop_schedule_override
from ..logic.gift_shop import build_gift_shops
from ..logic.gift_shop import resolve_gift_shop_context
from ..logic.gift_shop_schedule_conflict_resolution import save_gift_shop_opening_schedule_replacing_overlaps
from ..logic.gift_shop_schedule_conflict_resolution import save_gift_shop_opening_schedule_trimming_overlaps
from ..logic.gift_shop_status import build_gift_shop_closed_schedule
from ..logic.gift_shop_status import build_gift_shop_closure_override
from ..logic.gift_shop_status import build_gift_shop_opening_schedule
from ..logic.gift_shops_matching_query import build_gift_shops_matching_query
from ...models import GiftShop
from ...request_connection import get_connection
from ...types import DateInput, MonthInput, VisitDay, VisitYear


class GiftShopController():


   @classmethod
   def get_gift_shop_names( cls ) -> list[ str ]:
      return fetch_gift_shop_names( get_connection() )


   @classmethod
   def get_gift_shops(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         include_closed_gift_shops: bool,
         gift_shops_to_include: list[ str ] | None = None ) -> list[ GiftShop ]:

      context = resolve_gift_shop_context(
         day=day,
         month=month,
         year=year )

      return build_gift_shops(
         gift_shop_records=fetch_gift_shop_records(
            get_connection(),
            month=context.normalized_month,
            day=context.normalized_day ),
         schedule_records=fetch_gift_shop_schedule_records( get_connection() ),
         schedule_override_records=fetch_gift_shop_schedule_override_records(
            get_connection() ),
         context=context,
         include_closed_gift_shops=include_closed_gift_shops,
         gift_shops_to_include=gift_shops_to_include )


   @classmethod
   def get_gift_shops_matching_query(
         cls,
         query: str,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear ) -> list[ GiftShop ]:

      gift_shops = cls.get_gift_shops(
         day=day,
         month=month,
         year=year,
         include_closed_gift_shops=True )

      return build_gift_shops_matching_query(
         gift_shops,
         query )


   @classmethod
   def set_gift_shop_as_closed(
         cls,
         gift_shop: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:
      schedule = build_gift_shop_closed_schedule(
         gift_shop=gift_shop,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_gift_shop_opening_schedule(
         get_connection(),
         schedule=schedule )


   @classmethod
   def set_gift_shop_closure_override(
         cls,
         gift_shop: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:
      override = build_gift_shop_closure_override(
         gift_shop=gift_shop,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_gift_shop_schedule_override(
         get_connection(),
         override=override )


   @classmethod
   def set_gift_shop_opening_schedule(
         cls,
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
         message: str ) -> bool:
      schedule = build_gift_shop_opening_schedule(
         gift_shop=gift_shop,
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

      return save_gift_shop_opening_schedule(
         get_connection(),
         schedule=schedule )


   @classmethod
   def replace_gift_shop_opening_schedule_overlaps(
         cls,
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
         message: str ) -> bool:
      schedule = build_gift_shop_opening_schedule(
         gift_shop=gift_shop,
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

      return save_gift_shop_opening_schedule_replacing_overlaps(
         get_connection(),
         schedule=schedule )


   @classmethod
   def trim_gift_shop_opening_schedule_overlaps(
         cls,
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
         message: str ) -> bool:
      schedule = build_gift_shop_opening_schedule(
         gift_shop=gift_shop,
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

      return save_gift_shop_opening_schedule_trimming_overlaps(
         get_connection(),
         schedule=schedule )
