from __future__ import annotations

from ..scheduling.attraction_opening_schedule import AttractionOpeningSchedule
from ..scheduling.attraction_schedule_override import AttractionScheduleOverride
from ...shared.amenity_status_builders import AmenityStatusBuilders
from ...shared.enums import AmenityNameField
from ...types import Types


class AttractionStatusBuilder():
   _builders = AmenityStatusBuilders(
      name_field=AmenityNameField.ATTRACTION,
      opening_schedule_class=AttractionOpeningSchedule,
      schedule_override_class=AttractionScheduleOverride,
   )


   @classmethod
   def build_closed_schedule(
         cls,
         attraction: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> AttractionOpeningSchedule:
      return cls._builders.build_closed_schedule( attraction, start_date, end_date, message )


   @classmethod
   def build_opening_schedule(
         cls,
         attraction: str,
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
         message: str ) -> AttractionOpeningSchedule:
      return cls._builders.build_opening_schedule(
         attraction,
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
         attraction: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> AttractionScheduleOverride:
      return cls._builders.build_closure_override( attraction, start_date, end_date, message )
