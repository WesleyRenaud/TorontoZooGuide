from ..data_access.restaurant import fetch_restaurant_records
from ..data_access.restaurant import fetch_restaurant_schedule_records
from ..logic.restaurant import build_restaurants
from ..logic.restaurant import resolve_restaurant_context


class RestaurantController():
   def __init__( self, conn ):
      self._conn = conn


   def get_restaurants(
         self,
         month,
         day,
         include_closed_restaurants,
         restaurants_to_include=None ):

      context = resolve_restaurant_context(
         month=month,
         day=day )

      return build_restaurants(
         restaurant_records=fetch_restaurant_records(
            self._conn,
            month=context.normalized_month,
            day=context.normalized_day ),
         schedule_records=fetch_restaurant_schedule_records( self._conn ),
         context=context,
         include_closed_restaurants=include_closed_restaurants,
         restaurants_to_include=restaurants_to_include )
