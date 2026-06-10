from __future__ import annotations

from ..data_access.restaurant import fetch_restaurant_names
from ..data_access.restaurant import fetch_restaurant_records
from ..data_access.restaurant import fetch_restaurant_schedule_override_records
from ..data_access.restaurant import fetch_restaurant_schedule_records
from ..data_access.restaurant_schedule import save_restaurant_opening_schedule
from ..data_access.restaurant_schedule import save_restaurant_schedule_override
from ..logic.restaurant import build_restaurants
from ..logic.restaurant import resolve_restaurant_context
from ..logic.restaurant_schedule_conflict_resolution import save_restaurant_opening_schedule_replacing_overlaps
from ..logic.restaurant_schedule_conflict_resolution import save_restaurant_opening_schedule_trimming_overlaps
from ..logic.restaurant_status import build_restaurant_closed_schedule
from ..logic.restaurant_status import build_restaurant_closure_override
from ..logic.restaurant_status import build_restaurant_opening_schedule
from ..logic.restaurants_matching_query import build_restaurants_matching_query
from ...models import Restaurant
from ...request_connection import get_connection
from ...types import DateInput, MonthInput, VisitDay, VisitYear


class RestaurantCoordinator():


   @classmethod
   def get_restaurant_names( cls ) -> list[ str ]:
      return fetch_restaurant_names( get_connection() )


   @classmethod
   def get_restaurants(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         include_closed_restaurants: bool,
         restaurants_to_include: list[ str ] | None = None ) -> list[ Restaurant ]:

      context = resolve_restaurant_context(
         month=month,
         day=day,
         year=year )

      return build_restaurants(
         restaurant_records=fetch_restaurant_records(
            get_connection(),
            month=context.normalized_month,
            day=context.normalized_day ),
         schedule_records=fetch_restaurant_schedule_records( get_connection() ),
         schedule_override_records=fetch_restaurant_schedule_override_records(
            get_connection() ),
         context=context,
         include_closed_restaurants=include_closed_restaurants,
         restaurants_to_include=restaurants_to_include )


   @classmethod
   def get_restaurants_matching_query(
         cls,
         query: str,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         include_closed_restaurants: bool ) -> list[ Restaurant ]:

      restaurants = cls.get_restaurants(
         day=day,
         month=month,
         include_closed_restaurants=include_closed_restaurants,
         year=year )

      return build_restaurants_matching_query(
         restaurants,
         query )


   @classmethod
   def set_restaurant_as_closed(
         cls,
         restaurant: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:
      schedule = build_restaurant_closed_schedule(
         restaurant=restaurant,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_restaurant_opening_schedule(
         get_connection(),
         schedule=schedule )


   @classmethod
   def set_restaurant_closure_override(
         cls,
         restaurant: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:
      override = build_restaurant_closure_override(
         restaurant=restaurant,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_restaurant_schedule_override(
         get_connection(),
         override=override )


   @classmethod
   def set_restaurant_opening_schedule(
         cls,
         restaurant: str,
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
         get_connection(),
         schedule=schedule )


   @classmethod
   def replace_restaurant_opening_schedule_overlaps(
         cls,
         restaurant: str,
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

      return save_restaurant_opening_schedule_replacing_overlaps(
         get_connection(),
         schedule=schedule )


   @classmethod
   def trim_restaurant_opening_schedule_overlaps(
         cls,
         restaurant: str,
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

      return save_restaurant_opening_schedule_trimming_overlaps(
         get_connection(),
         schedule=schedule )
