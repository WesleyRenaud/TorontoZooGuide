from __future__ import annotations

from datetime import date

from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


class AttractionHoursSeenDays:
   weekday_records: list[ ZooHoursRecord ]
   weekend_records: list[ ZooHoursRecord ]


   def __init__( self ) -> None:
      self.weekday_records = []
      self.weekend_records = []


   def add( self, record: ZooHoursRecord ) -> date | None:
      day = DateValues.parse_date_value( record.operating_date )

      if day is None:
         return None

      if CalendarDates.is_weekend_or_holiday( d=day ):
         self.weekend_records.append( record )
      else:
         self.weekday_records.append( record )

      return day


   def both_day_kinds( self ) -> bool:
      return bool( self.weekday_records ) and bool( self.weekend_records )
