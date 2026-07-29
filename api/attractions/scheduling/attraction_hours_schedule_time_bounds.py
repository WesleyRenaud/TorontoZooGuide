from __future__ import annotations

from dataclasses import dataclass

from .attraction_hours_time_bounds import AttractionHoursTimeBounds
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...types import Connection, DateInput, DateKey, ScheduleTimeKey, TimeInput
from ...zoo_hours.data_access.zoo_hours import fetch_zoo_hours_records_between
from ...zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


@dataclass( frozen=True )
class AttractionHoursScheduleTimeBounds:
   weekday: AttractionHoursTimeBounds
   weekend_holiday: AttractionHoursTimeBounds


def _attraction_hours_time_bounds_from_records(
      records: list[ ZooHoursRecord ] ) -> AttractionHoursTimeBounds | None:
   if not records:
      return None

   open_record = max(
      records,
      key=lambda record: DateValues.time_value_in_seconds( record.open_time ) )
   close_record = min(
      records,
      key=lambda record: DateValues.time_value_in_seconds( record.close_time ) )

   return AttractionHoursTimeBounds(
      open_time=open_record.open_time,
      close_time=close_record.close_time,
      operating_date=close_record.operating_date )


def _records_for_day_kind(
      records: list[ ZooHoursRecord ],
      *,
      weekend_or_holiday: bool ) -> list[ ZooHoursRecord ]:
   matching: list[ ZooHoursRecord ] = []

   for record in records:
      operating_date = DateValues.parse_date_value( record.operating_date )

      if CalendarDates.is_weekend_or_holiday( d=operating_date ) == weekend_or_holiday:
         matching.append( record )

   return matching


def resolve_attraction_hours_schedule_date_range(
      start_date: DateInput,
      end_date: DateInput ) -> tuple[ DateKey, DateKey | None ]:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   return ( date_range.start_date, date_range.end_date )


def fetch_attraction_hours_schedule_time_bounds(
      conn: Connection,
      start_date: DateInput = None,
      end_date: DateInput = None ) -> AttractionHoursScheduleTimeBounds:
   range_start, range_end = resolve_attraction_hours_schedule_date_range(
      start_date,
      end_date )
   records = fetch_zoo_hours_records_between(
      conn,
      range_start,
      range_end )
   weekday_bounds = _attraction_hours_time_bounds_from_records(
      _records_for_day_kind( records, weekend_or_holiday=False ) )
   weekend_holiday_bounds = _attraction_hours_time_bounds_from_records(
      _records_for_day_kind( records, weekend_or_holiday=True ) )

   if weekday_bounds is None or weekend_holiday_bounds is None:
      raise ValueError( 'Could not resolve zoo hours bounds for attraction hours.' )

   return AttractionHoursScheduleTimeBounds(
      weekday=weekday_bounds,
      weekend_holiday=weekend_holiday_bounds )


def _time_is_within_attraction_hours_bounds(
      value: ScheduleTimeKey | TimeInput,
      bounds: AttractionHoursTimeBounds ) -> bool:
   return (
      DateValues.time_value_is_at_or_after( value, bounds.open_time )
      and not DateValues.time_value_is_after( value, bounds.close_time )
   )


def attraction_hours_schedule_times_are_within_bounds(
      bounds: AttractionHoursScheduleTimeBounds,
      *,
      weekday_start_time: TimeInput,
      weekday_end_time: TimeInput,
      weekend_holiday_start_time: TimeInput,
      weekend_holiday_end_time: TimeInput ) -> bool:
   return (
      _time_is_within_attraction_hours_bounds(
         weekday_start_time,
         bounds.weekday )
      and _time_is_within_attraction_hours_bounds(
         weekday_end_time,
         bounds.weekday )
      and _time_is_within_attraction_hours_bounds(
         weekend_holiday_start_time,
         bounds.weekend_holiday )
      and _time_is_within_attraction_hours_bounds(
         weekend_holiday_end_time,
         bounds.weekend_holiday )
   )
