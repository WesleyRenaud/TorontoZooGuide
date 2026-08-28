from __future__ import annotations

from ..scheduling.restaurant_opening_schedule import RestaurantOpeningSchedule
from ..scheduling.restaurant_schedule_override import RestaurantScheduleOverride
from ...shared.amenity_status_builders import AmenityStatusBuilders
from ...shared.enums import AmenityNameField
from ...types import Types


class RestaurantStatusBuilder():
   _builders = AmenityStatusBuilders(
      name_field=AmenityNameField.RESTAURANT,
      opening_schedule_class=RestaurantOpeningSchedule,
      schedule_override_class=RestaurantScheduleOverride,
   )


   @classmethod
   def build_closed_schedule(
         cls,
         restaurant: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> RestaurantOpeningSchedule:
      return cls._builders.build_closed_schedule( restaurant, start_date, end_date, message )


   @classmethod
   def build_opening_schedule(
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
         message: str ) -> RestaurantOpeningSchedule:
      return cls._builders.build_opening_schedule(
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
   def build_closure_override(
         cls,
         restaurant: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> RestaurantScheduleOverride:
      return cls._builders.build_closure_override( restaurant, start_date, end_date, message )
