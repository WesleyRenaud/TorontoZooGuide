from __future__ import annotations

from ...zoo_util import ZooUtil
from ...shared.strings import SharedStrings
from ...types import DateInput
from .animal_limited_viewing_schedule import AnimalLimitedViewingSchedule


def build_animal_limited_viewing_schedule(
      species: str,
      exhibit: str,
      start_date: DateInput,
      end_date: DateInput,
      daily_start_time: str,
      daily_end_time: str,
      message: str ) -> AnimalLimitedViewingSchedule:
   date_range = ZooUtil.resolve_open_ended_date_range(
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
   formatted_daily_start_time = ZooUtil.format_display_time_value(
      daily_start_time )
   formatted_daily_end_time = ZooUtil.format_display_time_value(
      daily_end_time )

   if end_date != None:
      return SharedStrings.Animals.limited_viewing_schedule_until(
         species=species,
         daily_start_time=formatted_daily_start_time,
         daily_end_time=formatted_daily_end_time,
         end_date=end_date )

   return SharedStrings.Animals.limited_viewing_schedule(
      species=species,
      daily_start_time=formatted_daily_start_time,
      daily_end_time=formatted_daily_end_time )
