from __future__ import annotations

from ..data_access.restaurant_provider import RestaurantProvider
from ..data_access.restaurant_schedule_provider import RestaurantScheduleProvider
from ..domain.restaurant_builder import RestaurantBuilder
from ...models import Restaurant
from ...request_connection import get_connection
from ..scheduling.restaurant_schedule_conflict_resolver import RestaurantScheduleConflictResolver
from ..search.restaurants_matching_query_builder import RestaurantsMatchingQueryBuilder
from ...shared.build_amenity_coordinator_mutations import AmenityCoordinatorMutations
from ..status.restaurant_status_builder import RestaurantStatusBuilder
from ...types import DateInput, MonthInput, VisitDay, VisitYear


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
      return RestaurantProvider.fetch_restaurant_names( get_connection() )


   @classmethod
   def get_restaurants(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         include_closed_restaurants: bool,
         restaurants_to_include: list[ str ] | None = None ) -> list[ Restaurant ]:

      context = RestaurantBuilder.resolve_context(
         month=month,
         day=day,
         year=year )

      return RestaurantBuilder.build_restaurants(
         restaurant_records=RestaurantProvider.fetch_restaurant_records(
            get_connection(),
            month=context.normalized_month,
            day=context.normalized_day ),
         schedule_records=RestaurantProvider.fetch_restaurant_schedule_records( get_connection() ),
         schedule_override_records=RestaurantProvider.fetch_restaurant_schedule_override_records(
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

      return RestaurantsMatchingQueryBuilder.build(
         restaurants,
         query )


   @classmethod
   def set_restaurant_as_closed(
         cls,
         restaurant: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:
      return _mutations.set_as_closed( restaurant, start_date, end_date, message )


   @classmethod
   def set_restaurant_closure_override(
         cls,
         restaurant: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:
      return _mutations.set_closure_override( restaurant, start_date, end_date, message )


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
