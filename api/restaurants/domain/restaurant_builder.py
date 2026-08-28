from __future__ import annotations

from datetime import date

from ..data_access.restaurant_record import RestaurantRecord
from ..data_access.restaurant_schedule_override_record import RestaurantScheduleOverrideRecord
from ..data_access.restaurant_schedule_record import RestaurantScheduleRecord
from ...models import Restaurant
from .restaurant_context import RestaurantContext
from ...shared.enums import ScheduleStatus
from ...shared.opening_schedule_seasonal_multiplier_resolver import OpeningScheduleSeasonalMultiplierResolver
from ...shared.opening_schedule_status_resolver import OpeningScheduleStatusResolver
from ...shared.opening_schedule_visit_context_resolver import OpeningScheduleVisitContextResolver
from ...types import MonthInput, SeasonalMultiplier, VisitDay, VisitYear


class RestaurantBuilder():
   @classmethod
   def resolve_context(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear ) -> RestaurantContext:
      return OpeningScheduleVisitContextResolver.resolve(
         day=day,
         month=month,
         year=year )


   @classmethod
   def calculate_likelihood(
         cls,
         day_seasonal_availability_multiplier: SeasonalMultiplier ) -> int:
      return OpeningScheduleStatusResolver.calculate_seasonal_likelihood( day_seasonal_availability_multiplier )


   @classmethod
   def group_schedule_records_by_name(
         cls,
         schedule_records: list[ RestaurantScheduleRecord ] ) -> dict[ str, list[ RestaurantScheduleRecord ] ]:
      return OpeningScheduleStatusResolver.group_records_by_name( schedule_records, lambda record: record.restaurant )


   @classmethod
   def group_schedule_override_records_by_name(
         cls,
         override_records: list[ RestaurantScheduleOverrideRecord ] ) -> dict[ str, list[ RestaurantScheduleOverrideRecord ] ]:
      return OpeningScheduleStatusResolver.group_records_by_name( override_records, lambda record: record.restaurant )


   @classmethod
   def is_open_on_day(
         cls,
         schedule_record: RestaurantScheduleRecord,
         weekday: int,
         is_holiday: bool ) -> bool:
      return OpeningScheduleStatusResolver.is_open_on_weekday(
         schedule_record=schedule_record,
         weekday=weekday,
         is_holiday=is_holiday )


   @classmethod
   def get_active_schedule_status(
         cls,
         schedule_records: list[ RestaurantScheduleRecord ],
         target_date: date,
         weekday: int ) -> tuple[ ScheduleStatus, str | None ]:
      return OpeningScheduleStatusResolver.get_active_opening_schedule_status(
         schedule_records=schedule_records,
         target_date=target_date,
         weekday=weekday )


   @classmethod
   def get_active_schedule_override_status(
         cls,
         override_records: list[ RestaurantScheduleOverrideRecord ],
         target_date: date ) -> tuple[ ScheduleStatus, str | None ]:
      return OpeningScheduleStatusResolver.get_active_schedule_override_status(
         override_records=override_records,
         target_date=target_date )


   @classmethod
   def get_day_seasonal_availability_multiplier(
         cls,
         restaurant_record: RestaurantRecord,
         context: RestaurantContext ) -> SeasonalMultiplier:
      return OpeningScheduleSeasonalMultiplierResolver.resolve(
         weekday_multiplier=restaurant_record.weekday_multiplier,
         weekend_holiday_multiplier=restaurant_record.weekend_holiday_multiplier,
         is_weekend_or_holiday=context.is_weekend_or_holiday )


   @classmethod
   def build_restaurant(
         cls,
         restaurant_record: RestaurantRecord,
         schedule_records: list[ RestaurantScheduleRecord ],
         schedule_override_records: list[ RestaurantScheduleOverrideRecord ],
         context: RestaurantContext ) -> Restaurant:

      likelihood, closed_message = OpeningScheduleStatusResolver.resolve_amenity_likelihood_and_message(
         name=restaurant_record.name,
         schedule_records=schedule_records,
         override_records=schedule_override_records,
         target_date=context.target_date,
         weekday=context.weekday,
         seasonal_multiplier=cls.get_day_seasonal_availability_multiplier(
            restaurant_record=restaurant_record,
            context=context ) )

      return Restaurant(
         name=restaurant_record.name,
         location=restaurant_record.location,
         sub_location=restaurant_record.sub_location,
         description=restaurant_record.description,
         menu_link=restaurant_record.menu_link,
         x_coord=restaurant_record.x_coord,
         y_coord=restaurant_record.y_coord,
         is_closed=likelihood <= 0,
         closed_message=closed_message,
         likelihood=likelihood )


   @classmethod
   def build_restaurants(
         cls,
         restaurant_records: list[ RestaurantRecord ],
         schedule_records: list[ RestaurantScheduleRecord ],
         schedule_override_records: list[ RestaurantScheduleOverrideRecord ],
         context: RestaurantContext,
         include_closed_restaurants: bool,
         restaurants_to_include: list[ str ] | None = None ) -> list[ Restaurant ]:

      restaurants_to_include = restaurants_to_include or []
      schedule_records_by_name = cls.group_schedule_records_by_name( schedule_records )
      schedule_override_records_by_name = cls.group_schedule_override_records_by_name(
         schedule_override_records )
      restaurants: list[ Restaurant ] = []

      for restaurant_record in restaurant_records:
         restaurant = cls.build_restaurant(
            restaurant_record=restaurant_record,
            schedule_records=schedule_records_by_name.get( restaurant_record.name, [] ),
            schedule_override_records=schedule_override_records_by_name.get(
               restaurant_record.name,
               [] ),
            context=context )

         if (
               include_closed_restaurants
               or not restaurant.is_closed
               or restaurant.name in restaurants_to_include ):
            restaurants.append( restaurant )

      return restaurants
