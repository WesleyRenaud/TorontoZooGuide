from __future__ import annotations

from ..data_access.gift_shop_provider import GiftShopProvider
from ..data_access.gift_shop_schedule_provider import GiftShopScheduleProvider
from ..domain.gift_shop_builder import GiftShopBuilder
from ...models import GiftShop
from ...request_connection_provider import RequestConnectionProvider
from ..scheduling.gift_shop_schedule_conflict_resolver import GiftShopScheduleConflictResolver
from ..search.gift_shops_matching_query_builder import GiftShopsMatchingQueryBuilder
from ...shared.amenity_coordinator_mutations import AmenityCoordinatorMutations
from ..status.gift_shop_status_builder import GiftShopStatusBuilder
from ...types import Types


_mutations = AmenityCoordinatorMutations(
   build_closed_schedule=GiftShopStatusBuilder.build_closed_schedule,
   build_opening_schedule=GiftShopStatusBuilder.build_opening_schedule,
   build_closure_override=GiftShopStatusBuilder.build_closure_override,
   save_opening_schedule=GiftShopScheduleProvider.save_opening_schedule,
   save_schedule_override=GiftShopScheduleProvider.save_schedule_override,
   save_replacing_overlaps=GiftShopScheduleConflictResolver.save_replacing_overlaps,
   save_trimming_overlaps=GiftShopScheduleConflictResolver.save_trimming_overlaps,
)


class GiftShopCoordinator():
   @classmethod
   def get_gift_shop_names( cls ) -> list[ str ]:
      return GiftShopProvider.fetch_gift_shop_names( RequestConnectionProvider.get() )


   @classmethod
   def get_gift_shops(
         cls,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear,
         include_closed_gift_shops: bool,
         gift_shops_to_include: list[ str ] | None = None ) -> list[ GiftShop ]:

      context = GiftShopBuilder.resolve_context(
         month=month,
         day=day,
         year=year )

      return GiftShopBuilder.build_gift_shops(
         gift_shop_records=GiftShopProvider.fetch_gift_shop_records(
            RequestConnectionProvider.get(),
            month=context.normalized_month,
            day=context.normalized_day ),
         schedule_records=GiftShopProvider.fetch_gift_shop_schedule_records( RequestConnectionProvider.get() ),
         schedule_override_records=GiftShopProvider.fetch_gift_shop_schedule_override_records(
            RequestConnectionProvider.get() ),
         context=context,
         include_closed_gift_shops=include_closed_gift_shops,
         gift_shops_to_include=gift_shops_to_include )


   @classmethod
   def get_gift_shops_matching_query(
         cls,
         query: str,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear ) -> list[ GiftShop ]:

      gift_shops = cls.get_gift_shops(
         day=day,
         month=month,
         year=year,
         include_closed_gift_shops=True )

      return GiftShopsMatchingQueryBuilder.build(
         gift_shops,
         query )


   @classmethod
   def set_gift_shop_as_closed(
         cls,
         gift_shop: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      return _mutations.set_as_closed( gift_shop, start_date, end_date, message )


   @classmethod
   def set_gift_shop_closure_override(
         cls,
         gift_shop: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      return _mutations.set_closure_override( gift_shop, start_date, end_date, message )


   @classmethod
   def set_gift_shop_opening_schedule(
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
