from __future__ import annotations

from .attraction_hours_schedule_time_bounds import AttractionHoursScheduleTimeBounds
from .attraction_hours_time_bounds import AttractionHoursTimeBounds
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...types import Connection, DateInput, DateKey, ScheduleTimeKey, TimeInput
from ...zoo_hours.data_access.zoo_hours_provider import ZooHoursProvider
from ...zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


class AttractionHoursScheduleTimeBoundsBuilder():
   @classmethod
   def _build_time_bounds(
         cls,
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


   @classmethod
   def _records_for_day_kind(
         cls,
         records: list[ ZooHoursRecord ],
         *,
         weekend_or_holiday: bool ) -> list[ ZooHoursRecord ]:
      matching: list[ ZooHoursRecord ] = []
      for record in records:
         operating_date = DateValues.parse_date_value( record.operating_date )
         if CalendarDates.is_weekend_or_holiday( d=operating_date ) == weekend_or_holiday:
            matching.append( record )
      return matching


   @classmethod
   def resolve_date_range(
         cls,
         start_date: DateInput,
         end_date: DateInput ) -> tuple[ DateKey, DateKey | None ]:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )
      return ( date_range.start_date, date_range.end_date )


   @classmethod
   def fetch(
         cls,
         conn: Connection,
         start_date: DateInput = None,
         end_date: DateInput = None ) -> AttractionHoursScheduleTimeBounds:
      range_start, range_end = cls.resolve_date_range( start_date, end_date )
      records = ZooHoursProvider.fetch_zoo_hours_records_between( conn, range_start, range_end )
      weekday_bounds = cls._build_time_bounds(
         cls._records_for_day_kind( records, weekend_or_holiday=False ) )
      weekend_holiday_bounds = cls._build_time_bounds(
         cls._records_for_day_kind( records, weekend_or_holiday=True ) )
      if weekday_bounds is None or weekend_holiday_bounds is None:
         raise ValueError( 'Could not resolve zoo hours bounds for attraction hours.' )
      return AttractionHoursScheduleTimeBounds(
         weekday=weekday_bounds,
         weekend_holiday=weekend_holiday_bounds )


   @classmethod
   def _time_is_within_bounds(
         cls,
         value: ScheduleTimeKey | TimeInput,
         bounds: AttractionHoursTimeBounds ) -> bool:
      return (
         DateValues.time_value_is_at_or_after( value, bounds.open_time )
         and not DateValues.time_value_is_after( value, bounds.close_time )
      )


   @classmethod
   def times_are_within_bounds(
         cls,
         bounds: AttractionHoursScheduleTimeBounds,
         *,
         weekday_start_time: TimeInput,
         weekday_end_time: TimeInput,
         weekend_holiday_start_time: TimeInput,
         weekend_holiday_end_time: TimeInput ) -> bool:
      return (
         cls._time_is_within_bounds( weekday_start_time, bounds.weekday )
         and cls._time_is_within_bounds( weekday_end_time, bounds.weekday )
         and cls._time_is_within_bounds(
            weekend_holiday_start_time,
            bounds.weekend_holiday )
         and cls._time_is_within_bounds(
            weekend_holiday_end_time,
            bounds.weekend_holiday )
      )
