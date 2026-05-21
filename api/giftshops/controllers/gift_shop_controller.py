from ..data_access.gift_shop import fetch_gift_shop_names
from ..data_access.gift_shop import fetch_gift_shop_records
from ..data_access.gift_shop import fetch_gift_shop_schedule_records
from ..data_access.gift_shop_schedule import save_gift_shop_opening_schedule
from ..logic.gift_shop import build_gift_shops
from ..logic.gift_shop import resolve_gift_shop_context
from ..logic.gift_shop_status import build_gift_shop_closed_schedule
from ..logic.gift_shop_status import build_gift_shop_opening_schedule
from ..logic.gift_shops_matching_query import build_gift_shops_matching_query


class GiftShopController():
   def __init__( self, conn ):
      self._conn = conn


   def get_gift_shop_names( self ):
      return fetch_gift_shop_names( self._conn )


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


   def set_gift_shop_as_closed(
         self,
         gift_shop,
         start_date,
         end_date,
         message ):
      schedule = build_gift_shop_closed_schedule(
         gift_shop=gift_shop,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_gift_shop_opening_schedule(
         self._conn,
         schedule=schedule )


   def set_gift_shop_opening_schedule(
         self,
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
         self._conn,
         schedule=schedule )
