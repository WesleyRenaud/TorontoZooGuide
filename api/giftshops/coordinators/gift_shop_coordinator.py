from __future__ import annotations

from ..data_access.gift_shop import fetch_gift_shop_names
from ..data_access.gift_shop import fetch_gift_shop_records
from ..data_access.gift_shop import fetch_gift_shop_schedule_override_records
from ..data_access.gift_shop import fetch_gift_shop_schedule_records
from ..data_access.gift_shop_schedule import save_gift_shop_opening_schedule
from ..data_access.gift_shop_schedule import save_gift_shop_schedule_override
from ..domain.gift_shop import build_gift_shops
from ..domain.gift_shop import resolve_gift_shop_context
from ...models import GiftShop
from ...request_connection import get_connection
from ..scheduling.gift_shop_schedule_conflict_resolution import save_gift_shop_opening_schedule_replacing_overlaps
from ..scheduling.gift_shop_schedule_conflict_resolution import save_gift_shop_opening_schedule_trimming_overlaps
from ..search.gift_shops_matching_query import build_gift_shops_matching_query
from ...shared.build_amenity_coordinator_mutations import AmenityCoordinatorMutations
from ..status.gift_shop_status import build_gift_shop_closed_schedule
from ..status.gift_shop_status import build_gift_shop_closure_override
from ..status.gift_shop_status import build_gift_shop_opening_schedule
from ...types import DateInput, MonthInput, VisitDay, VisitYear


_mutations = AmenityCoordinatorMutations(
   build_closed_schedule=build_gift_shop_closed_schedule,
   build_opening_schedule=build_gift_shop_opening_schedule,
   build_closure_override=build_gift_shop_closure_override,
   save_opening_schedule=save_gift_shop_opening_schedule,
   save_schedule_override=save_gift_shop_schedule_override,
   save_replacing_overlaps=save_gift_shop_opening_schedule_replacing_overlaps,
   save_trimming_overlaps=save_gift_shop_opening_schedule_trimming_overlaps,
)


class GiftShopCoordinator():
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
      return _mutations.set_as_closed( gift_shop, start_date, end_date, message )


   @classmethod
   def set_gift_shop_closure_override(
         cls,
         gift_shop: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:
      return _mutations.set_closure_override( gift_shop, start_date, end_date, message )


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
      return _mutations.set_opening_schedule(
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
      return _mutations.replace_opening_schedule_overlaps(
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
      return _mutations.trim_opening_schedule_overlaps(
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
