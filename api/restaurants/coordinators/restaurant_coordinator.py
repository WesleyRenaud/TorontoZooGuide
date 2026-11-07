from __future__ import annotations

from ..data_access.restaurant_closure_record import RestaurantClosureRecord
from ..data_access.restaurant_provider import RestaurantProvider
from ..data_access.restaurant_schedule_provider import RestaurantScheduleProvider
from ..data_access.restaurant_status_provider import RestaurantStatusProvider
from ..domain.restaurant_builder import RestaurantBuilder
from ..domain.restaurant_menu_link import RestaurantMenuLink
from ..domain.seasonal_restaurant import SeasonalRestaurant
from ..domain.seasonal_restaurant_builder import SeasonalRestaurantBuilder
from ...models import Restaurant
from ...request_connection_provider import RequestConnectionProvider
from ..scheduling.restaurant_schedule_conflict_resolver import RestaurantScheduleConflictResolver
from ..search.restaurants_matching_query_builder import RestaurantsMatchingQueryBuilder
from ...shared.amenity_coordinator_mutations import AmenityCoordinatorMutations
from ...shared.calendar_dates import DateValues
from ..status.restaurant_season_closure_builder import RestaurantSeasonClosureBuilder
from ..status.restaurant_status_builder import RestaurantStatusBuilder
from ...types import Types


_mutations = AmenityCoordinatorMutations(
   build_closed_schedule=RestaurantStatusBuilder.build_closed_schedule,
   build_opening_schedule=RestaurantStatusBuilder.build_opening_schedule,
   build_closure_override=RestaurantStatusBuilder.build_closure_override,
   save_opening_schedule=RestaurantScheduleProvider.save_opening_schedule,
   save_schedule_override=RestaurantScheduleProvider.save_schedule_override,
   save_replacing_overlaps=RestaurantScheduleConflictResolver.save_replacing_overlaps,
   save_trimming_overlaps=RestaurantScheduleConflictResolver.save_trimming_overlaps,
)


class RestaurantCoordinator():
   @classmethod
   def get_restaurant_names( cls ) -> list[ str ]:
      return RestaurantProvider.fetch_restaurant_names( RequestConnectionProvider.get() )


   @classmethod
   def get_restaurant_menu_links( cls ) -> list[ RestaurantMenuLink ]:
      return RestaurantProvider.fetch_restaurant_menu_links( RequestConnectionProvider.get() )


   @classmethod
   def get_restaurants(
         cls,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear,
         include_closed_restaurants: bool,
         restaurants_to_include: list[ str ] | None = None ) -> list[ Restaurant ]:

      context = RestaurantBuilder.resolve_context(
         month=month,
         day=day,
         year=year )

      return RestaurantBuilder.build_restaurants(
         restaurant_records=RestaurantProvider.fetch_restaurant_records(
            RequestConnectionProvider.get(),
            month=context.normalized_month,
            day=context.normalized_day ),
         schedule_records=RestaurantProvider.fetch_restaurant_schedule_records( RequestConnectionProvider.get() ),
         schedule_override_records=RestaurantProvider.fetch_restaurant_schedule_override_records(
            RequestConnectionProvider.get() ),
         context=context,
         include_closed_restaurants=include_closed_restaurants,
         restaurants_to_include=restaurants_to_include,
         closure_records=RestaurantStatusProvider.fetch_closure_records(
            RequestConnectionProvider.get() ) )


   @classmethod
   def get_restaurants_matching_query(
         cls,
         query: str,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear,
         include_closed_restaurants: bool ) -> list[ Restaurant ]:

      restaurants = cls.get_restaurants(
         day=day,
         month=month,
         include_closed_restaurants=include_closed_restaurants,
         year=year )

      return RestaurantsMatchingQueryBuilder.build(
         restaurants,
         query )


   @classmethod
   def get_closure_records( cls ) -> list[ RestaurantClosureRecord ]:
      return RestaurantStatusProvider.fetch_closure_records( RequestConnectionProvider.get() )


   @classmethod
   def get_seasonal_restaurants( cls ) -> list[ SeasonalRestaurant ]:
      return SeasonalRestaurantBuilder.build(
         restaurants=cls.get_restaurant_menu_links(),
         closure_records=cls.get_closure_records(),
      )


   @classmethod
   def get_closed_for_season_restaurant_names( cls ) -> list[ str ]:
      return RestaurantStatusProvider.fetch_closed_for_season_names(
         RequestConnectionProvider.get(),
         today=DateValues.today_date_key() )


   @classmethod
   def set_restaurant_as_closed_for_season(
         cls,
         restaurant: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      status = RestaurantSeasonClosureBuilder.build(
         restaurant=restaurant,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return RestaurantStatusProvider.save_closed_for_season(
         RequestConnectionProvider.get(),
         restaurant=status.restaurant,
         start_date=status.start_date,
         end_date=status.end_date,
         message=status.message )


   @classmethod
   def set_restaurant_as_open_for_season( cls, restaurant: str ) -> bool:
      return RestaurantStatusProvider.delete_closed_for_season(
         RequestConnectionProvider.get(),
         restaurant=restaurant )


   @classmethod
   def set_restaurant_as_closed(
         cls,
         restaurant: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      return _mutations.set_as_closed( restaurant, start_date, end_date, message )


   @classmethod
   def set_restaurant_closure_override(
         cls,
         restaurant: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      return _mutations.set_closure_override( restaurant, start_date, end_date, message )


   @classmethod
   def set_restaurant_opening_schedule(
         cls,
         restaurant: str,
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
         message )


   @classmethod
   def replace_restaurant_opening_schedule_overlaps(
         cls,
         restaurant: str,
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
         message )


   @classmethod
   def trim_restaurant_opening_schedule_overlaps(
         cls,
         restaurant: str,
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
         message )
