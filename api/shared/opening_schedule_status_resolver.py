from __future__ import annotations

from collections.abc import Callable
from datetime import date
from typing import TypeVar

from ..app_strings import format_app_string
from .calendar_dates import CalendarDates
from .calendar_dates import DateValues
from .enums import ScheduleStatus
from .opening_schedule_record import OpeningScheduleRecord
from .schedule_override_record import ScheduleOverrideRecord
from ..types import SeasonalMultiplier


TRecord = TypeVar( 'TRecord' )


class OpeningScheduleStatusResolver():
   @classmethod
   def group_records_by_name(
         cls,
         records: list[ TRecord ],
         get_name: Callable[ [ TRecord ], str ],
   ) -> dict[ str, list[ TRecord ] ]:
      records_by_name: dict[ str, list[ TRecord ] ] = {}

      for record in records:
         name = get_name( record )

         if name not in records_by_name:
            records_by_name[ name ] = []

         records_by_name[ name ].append( record )

      return records_by_name


   @classmethod
   def is_open_on_weekday(
         cls,
         schedule_record: OpeningScheduleRecord,
         weekday: int,
         is_holiday: bool ) -> bool:
      weekday_values = [
         schedule_record.monday,
         schedule_record.tuesday,
         schedule_record.wednesday,
         schedule_record.thursday,
         schedule_record.friday,
         schedule_record.saturday,
         schedule_record.sunday,
      ]

      return (
         bool( weekday_values[ weekday ] )
         or ( is_holiday and schedule_record.holidays_only ) )


   @classmethod
   def get_active_opening_schedule_status(
         cls,
         schedule_records: list[ OpeningScheduleRecord ],
         target_date: date,
         weekday: int,
         *,
         build_closed_message: Callable[ [ OpeningScheduleRecord ], str | None ] | None = None,
   ) -> tuple[ ScheduleStatus, str | None ]:
      if len( schedule_records ) == 0:
         return ScheduleStatus.UNKNOWN, None

      for schedule_record in schedule_records:
         is_active = DateValues.is_date_in_range(
            target_date=target_date,
            start_date_value=schedule_record.schedule_start_date,
            end_date_value=schedule_record.schedule_end_date )

         if not is_active:
            continue

         is_holiday = CalendarDates.is_holiday( d=target_date )

         if cls.is_open_on_weekday(
               schedule_record=schedule_record,
               weekday=weekday,
               is_holiday=is_holiday ):
            return ScheduleStatus.OPEN, None

         if build_closed_message is not None:
            return ScheduleStatus.CLOSED, build_closed_message( schedule_record )

         return ScheduleStatus.CLOSED, schedule_record.schedule_message

      return ScheduleStatus.UNKNOWN, None


   @classmethod
   def get_active_schedule_override_status(
         cls,
         override_records: list[ ScheduleOverrideRecord ],
         target_date: date ) -> tuple[ ScheduleStatus, str | None ]:
      for override_record in override_records:
         is_active = DateValues.is_date_in_range(
            target_date=target_date,
            start_date_value=override_record.override_start_date,
            end_date_value=override_record.override_end_date )

         if not is_active:
            continue

         if override_record.is_closed:
            return ScheduleStatus.CLOSED, override_record.override_message

         return ScheduleStatus.OPEN, None

      return ScheduleStatus.UNKNOWN, None


   @classmethod
   def calculate_seasonal_likelihood(
         cls,
         day_seasonal_availability_multiplier: SeasonalMultiplier ) -> int:
      seasonal_multiplier = (
         day_seasonal_availability_multiplier
         if day_seasonal_availability_multiplier is not None
         else 1.0
      )
      likelihood = max( 0.0, min( seasonal_multiplier, 1.0 ) )

      return max( round( likelihood * 100 ), 0 )


   @classmethod
   def resolve_amenity_likelihood_and_message(
         cls,
         *,
         name: str,
         schedule_records: list[ OpeningScheduleRecord ],
         override_records: list[ ScheduleOverrideRecord ],
         target_date: date,
         weekday: int,
         seasonal_multiplier: SeasonalMultiplier,
         build_closed_schedule_message: Callable[ [ OpeningScheduleRecord ], str | None ] | None = None,
         likely_closed_message: Callable[ [ str ], str ] | None = None,
   ) -> tuple[ int, str | None ]:
      likelihood = 100
      closed_message = None

      override_status, override_message = cls.get_active_schedule_override_status(
         override_records=override_records,
         target_date=target_date )

      if override_status == ScheduleStatus.CLOSED:
         return 0, override_message

      schedule_status, schedule_message = cls.get_active_opening_schedule_status(
         schedule_records=schedule_records,
         target_date=target_date,
         weekday=weekday,
         build_closed_message=build_closed_schedule_message )

      if schedule_status == ScheduleStatus.CLOSED:
         likelihood = 0
         closed_message = schedule_message
      elif schedule_status == ScheduleStatus.UNKNOWN:
         likelihood = cls.calculate_seasonal_likelihood( seasonal_multiplier )

         if likelihood == 0:
            if likely_closed_message is not None:
               closed_message = likely_closed_message( name )
            else:
               closed_message = format_app_string( 'guestStatus.locations.likelyNotOpenOnDay', name=name )

      return likelihood, closed_message
