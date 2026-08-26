from __future__ import annotations

from datetime import date

from ..data_access.attraction_provider import AttractionProvider
from ..data_access.attraction_record import AttractionRecord
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...shared.operating_hours import OperatingHours
from ...types import Connection
from ...types import ScheduleTimeKey


class AttractionOperatingHoursResolver():
   @classmethod
   def has_configured_operating_hours(
         cls,
         attraction_record: AttractionRecord,
         *,
         visit_date: date ) -> bool:
      start_time, end_time = cls._configured_hours_for_visit_date(
         attraction_record,
         visit_date=visit_date )
      return start_time is not None or end_time is not None


   @classmethod
   def operating_hours_seconds(
         cls,
         attraction_record: AttractionRecord,
         *,
         visit_date: date,
         zoo_operating_hours: OperatingHours ) -> OperatingHours:
      start_time, end_time = cls._configured_hours_for_visit_date(
         attraction_record,
         visit_date=visit_date )
      open_seconds = DateValues.time_value_in_seconds( start_time )
      close_seconds = DateValues.time_value_in_seconds( end_time )
      if open_seconds is None:
         open_seconds = zoo_operating_hours.open_seconds
      if close_seconds is None:
         close_seconds = zoo_operating_hours.close_seconds
      return OperatingHours(
         open_seconds=open_seconds,
         close_seconds=close_seconds )


   @classmethod
   def fetch_configured_operating_hours_seconds(
         cls,
         conn: Connection,
         attraction_name: str,
         *,
         visit_date: date,
         zoo_operating_hours: OperatingHours ) -> OperatingHours | None:
      attraction_record = AttractionProvider.fetch_attraction_record_for_calendar_day(
         conn,
         attraction_name,
         visit_date )
      if attraction_record is None:
         return None
      if not cls.has_configured_operating_hours(
            attraction_record,
            visit_date=visit_date ):
         return None
      return cls.operating_hours_seconds(
         attraction_record,
         visit_date=visit_date,
         zoo_operating_hours=zoo_operating_hours )


   @classmethod
   def _configured_hours_for_visit_date(
         cls,
         attraction_record: AttractionRecord,
         *,
         visit_date: date ) -> tuple[ ScheduleTimeKey, ScheduleTimeKey ]:
      if CalendarDates.is_weekend_or_holiday( d=visit_date ):
         return (
            attraction_record.weekend_holiday_start_time,
            attraction_record.weekend_holiday_end_time )
      return (
         attraction_record.weekday_start_time,
         attraction_record.weekday_end_time )
