from __future__ import annotations

from datetime import date

from ..data_access.attraction_record import AttractionRecord
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...types import ScheduleTimeKey


def attraction_has_configured_operating_hours(
      attraction_record: AttractionRecord,
      *,
      visit_date: date ) -> bool:
   start_time, end_time = _configured_hours_for_visit_date(
      attraction_record,
      visit_date=visit_date )
   return start_time is not None or end_time is not None


def attraction_operating_hours_seconds(
      attraction_record: AttractionRecord,
      *,
      visit_date: date,
      zoo_open_seconds: int,
      zoo_close_seconds: int,
   ) -> tuple[ int, int ]:
   """Return open/close seconds for the visit day.

   Configured weekday or weekend/holiday times win when present. Missing sides
   fall back to zoo hours. Attractions with no configured hours use full zoo
   hours.
   """
   start_time, end_time = _configured_hours_for_visit_date(
      attraction_record,
      visit_date=visit_date )
   open_seconds = DateValues.time_value_in_seconds( start_time )
   close_seconds = DateValues.time_value_in_seconds( end_time )

   if open_seconds is None:
      open_seconds = zoo_open_seconds

   if close_seconds is None:
      close_seconds = zoo_close_seconds

   return open_seconds, close_seconds


def _configured_hours_for_visit_date(
      attraction_record: AttractionRecord,
      *,
      visit_date: date,
   ) -> tuple[ ScheduleTimeKey, ScheduleTimeKey ]:
   if CalendarDates.is_weekend_or_holiday( d=visit_date ):
      return (
         attraction_record.weekend_holiday_start_time,
         attraction_record.weekend_holiday_end_time )

   return (
      attraction_record.weekday_start_time,
      attraction_record.weekday_end_time )
