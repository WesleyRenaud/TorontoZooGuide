from __future__ import annotations

from .attraction_hours_clock import AttractionHoursClock
from .attraction_hours_coverage import AttractionHoursCoverage
from .attraction_hours_schedule_time_bounds import AttractionHoursScheduleTimeBounds
from .attraction_hours_seen_days import AttractionHoursSeenDays
from .attraction_hours_segment import AttractionHoursSegment
from .attraction_hours_span import AttractionHoursSpan
from .attraction_hours_time_bounds import AttractionHoursTimeBounds
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...types import Types
from ...zoo_hours.data_access.zoo_hours_provider import ZooHoursProvider
from ...zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


class AttractionHoursScheduleTimeBoundsBuilder():
   @classmethod
   def _build_time_bounds(
         cls,
         records: list[ ZooHoursRecord ] ) -> AttractionHoursTimeBounds | None:
      if not records:
         return None

      return cls._tightest_bounds( records )


   @classmethod
   def _tightest_bounds(
         cls,
         records: list[ ZooHoursRecord ] ) -> AttractionHoursTimeBounds:
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
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> tuple[ Types.DateKey, Types.DateKey | None ]:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )
      return ( date_range.start_date, date_range.end_date )


   @classmethod
   def fetch(
         cls,
         conn: Types.Connection,
         start_date: Types.DateInput = None,
         end_date: Types.DateInput = None ) -> AttractionHoursScheduleTimeBounds | None:
      range_start, range_end = cls.resolve_date_range( start_date, end_date )
      records = ZooHoursProvider.fetch_zoo_hours_records_between( conn, range_start, range_end )
      weekday_records = cls._records_for_day_kind( records, weekend_or_holiday=False )
      weekend_records = cls._records_for_day_kind( records, weekend_or_holiday=True )

      if not weekday_records or not weekend_records:
         return None

      return cls._schedule_bounds( weekday_records, weekend_records )


   @classmethod
   def hours_fall_within(
         cls,
         conn: Types.Connection,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         *,
         weekday_start_time: Types.TimeInput,
         weekday_end_time: Types.TimeInput,
         weekend_holiday_start_time: Types.TimeInput,
         weekend_holiday_end_time: Types.TimeInput ) -> bool:
      bounds = cls.fetch( conn, start_date=start_date, end_date=end_date )

      if bounds is None:
         return False

      return cls.times_are_within_bounds(
         bounds,
         weekday_start_time=weekday_start_time,
         weekday_end_time=weekday_end_time,
         weekend_holiday_start_time=weekend_holiday_start_time,
         weekend_holiday_end_time=weekend_holiday_end_time )


   @classmethod
   def _schedule_bounds(
         cls,
         weekday_records: list[ ZooHoursRecord ],
         weekend_records: list[ ZooHoursRecord ] ) -> AttractionHoursScheduleTimeBounds:
      return AttractionHoursScheduleTimeBounds(
         weekday=cls._tightest_bounds( weekday_records ),
         weekend_holiday=cls._tightest_bounds( weekend_records ) )


   @classmethod
   def _clock_fits(
         cls,
         clock: AttractionHoursClock,
         seen: AttractionHoursSeenDays ) -> bool:
      return cls.times_are_within_bounds(
         cls._schedule_bounds( seen.weekday_records, seen.weekend_records ),
         weekday_start_time=clock.weekday_start_time,
         weekday_end_time=clock.weekday_end_time,
         weekend_holiday_start_time=clock.weekend_holiday_start_time,
         weekend_holiday_end_time=clock.weekend_holiday_end_time )


   @classmethod
   def _coverage(
         cls,
         records: list[ ZooHoursRecord ],
         clock: AttractionHoursClock ) -> AttractionHoursCoverage:
      seen = AttractionHoursSeenDays()
      stops_fitting_on = None

      for record in records:
         day = seen.add( record )

         if day is None or not seen.both_day_kinds():
            continue

         if cls._clock_fits( clock, seen ):
            continue

         stops_fitting_on = day
         break

      return AttractionHoursCoverage(
         stops_fitting_on=stops_fitting_on,
         both_day_kinds=seen.both_day_kinds() )


   @classmethod
   def _zoo_hour_records(
         cls,
         conn: Types.Connection,
         span: AttractionHoursSpan ) -> list[ ZooHoursRecord ]:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=span.start,
         end_date=span.end )
      return ZooHoursProvider.fetch_zoo_hours_records_between(
         conn,
         date_range.start_date,
         date_range.end_date )


   @classmethod
   def fitting_spans(
         cls,
         conn: Types.Connection,
         span: AttractionHoursSpan,
         clock: AttractionHoursClock ) -> list[ AttractionHoursSpan ]:
      spans: list[ AttractionHoursSpan ] = []
      start = span.start

      for segment in AttractionHoursSegment.split_on_christmas( cls._zoo_hour_records( conn, span ) ):
         coverage = cls._coverage( segment.records, clock )
         fitted = segment.fitted_span( start, span.end, coverage )

         if fitted is not None:
            spans.append( fitted )

         christmas = segment.christmas

         if christmas is None or coverage.stops_fitting_on is not None:
            break

         start = CalendarDates.one_day_later( christmas )

      return spans


   @classmethod
   def _time_is_within_bounds(
         cls,
         value: Types.ScheduleTimeKey | Types.TimeInput,
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
         weekday_start_time: Types.TimeInput,
         weekday_end_time: Types.TimeInput,
         weekend_holiday_start_time: Types.TimeInput,
         weekend_holiday_end_time: Types.TimeInput ) -> bool:
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
