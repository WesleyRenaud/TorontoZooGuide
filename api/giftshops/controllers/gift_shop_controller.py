from ..data_access.gift_shop import fetch_gift_shop_records
from ..data_access.gift_shop import fetch_gift_shop_schedule_records
from ..logic.gift_shop import build_gift_shops
from ..logic.gift_shop import resolve_gift_shop_context
from ..logic.gift_shops_matching_query import build_gift_shops_matching_query


class GiftShopController():
   def __init__( self, conn ):
      self._conn = conn


   def get_gift_shops(
         self,
         day,
         month,
         year,
         include_closed_gift_shops,
         gift_shops_to_include=None ):

      context = resolve_gift_shop_context(
         day=day,
         month=month,
         year=year )

      return build_gift_shops(
         gift_shop_records=fetch_gift_shop_records(
            self._conn,
            month=context.normalized_month,
            day=context.normalized_day ),
         schedule_records=fetch_gift_shop_schedule_records( self._conn ),
         context=context,
         include_closed_gift_shops=include_closed_gift_shops,
         gift_shops_to_include=gift_shops_to_include )


   def get_gift_shops_matching_query(
         self,
         query,
         day,
         month,
         year ):

      gift_shops = self.get_gift_shops(
         day=day,
         month=month,
         year=year,
         include_closed_gift_shops=True )

      return build_gift_shops_matching_query(
         gift_shops,
         query )
