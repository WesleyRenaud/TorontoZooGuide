from ..data_access.restaurant import fetch_restaurant_names
from ..data_access.restaurant import fetch_restaurant_records
from ..data_access.restaurant import fetch_restaurant_schedule_records
from ..data_access.restaurant_schedule import save_restaurant_opening_schedule
from ..logic.restaurant import build_restaurants
from ..logic.restaurant import resolve_restaurant_context
from ..logic.restaurant_status import build_restaurant_closed_schedule
from ..logic.restaurant_status import build_restaurant_opening_schedule
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


   def set_restaurant_as_closed(
         self,
         restaurant,
         start_date,
         end_date,
         message ):
      schedule = build_restaurant_closed_schedule(
         restaurant=restaurant,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_restaurant_opening_schedule(
         self._conn,
         schedule=schedule )


   def set_restaurant_opening_schedule(
         self,
         restaurant,
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
      schedule = build_restaurant_opening_schedule(
         restaurant=restaurant,
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

      return save_restaurant_opening_schedule(
         self._conn,
         schedule=schedule )
