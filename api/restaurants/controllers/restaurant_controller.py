from ..data_access.restaurant import fetch_restaurant_names
from ..data_access.restaurant import fetch_restaurant_records
from ..data_access.restaurant import fetch_restaurant_schedule_records
from ..logic.restaurant import build_restaurants
from ..logic.restaurant import resolve_restaurant_context
from ..logic.restaurants_matching_query import build_restaurants_matching_query


class RestaurantController():
   def __init__( self, conn ):
      self._conn = conn


   def get_restaurant_names( self ):
      return fetch_restaurant_names( self._conn )


   def get_restaurants(
         self,
         day,
         month,
         year,
         include_closed_restaurants,
         restaurants_to_include=None ):

      context = resolve_restaurant_context(
         month=month,
         day=day,
         year=year )

      return build_restaurants(
         restaurant_records=fetch_restaurant_records(
            self._conn,
            month=context.normalized_month,
            day=context.normalized_day ),
         schedule_records=fetch_restaurant_schedule_records( self._conn ),
         context=context,
         include_closed_restaurants=include_closed_restaurants,
         restaurants_to_include=restaurants_to_include )


   def get_restaurants_matching_query(
         self,
         query,
         day,
         month,
         year,
         include_closed_restaurants ):

      restaurants = self.get_restaurants(
         day=day,
         month=month,
         include_closed_restaurants=include_closed_restaurants,
         year=year )

      return build_restaurants_matching_query(
         restaurants,
         query )
