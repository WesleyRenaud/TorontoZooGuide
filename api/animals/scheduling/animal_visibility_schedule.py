from __future__ import annotations

from .animal_limited_viewing_schedule import AnimalLimitedViewingSchedule
from ...app_strings import format_app_string
from ...shared.calendar_dates import DateValues
from ...types import DateInput


def build_animal_limited_viewing_schedule(
      species: str,
      exhibit: str,
      start_date: DateInput,
      end_date: DateInput,
      daily_start_time: str,
      daily_end_time: str,
      message: str ) -> AnimalLimitedViewingSchedule:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = build_limited_viewing_schedule_message(
         species=species,
         daily_start_time=daily_start_time,
         daily_end_time=daily_end_time,
         end_date=date_range.end_date )

   return AnimalLimitedViewingSchedule(
      species=species,
      exhibit=exhibit,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      daily_start_time=daily_start_time,
      daily_end_time=daily_end_time,
      message=message )


def build_limited_viewing_schedule_message(
      species: str,
      daily_start_time: str,
      daily_end_time: str,
      end_date: DateInput ) -> str:
   formatted_daily_start_time = DateValues.format_display_time_value(
      daily_start_time )
   formatted_daily_end_time = DateValues.format_display_time_value(
      daily_end_time )

   if end_date != None:
      return format_app_string(
         'guestStatus.animals.limitedViewingScheduleUntil',
         species=species,
         dailyStartTime=formatted_daily_start_time,
         dailyEndTime=formatted_daily_end_time,
         endDate=DateValues.format_display_date_value( end_date ) )

   return format_app_string(
      'guestStatus.animals.limitedViewingSchedule',
      species=species,
      dailyStartTime=formatted_daily_start_time,
      dailyEndTime=formatted_daily_end_time )
