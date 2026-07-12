from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Self

from .calendar_dates import DateValues
from .value_conversion import ValueConversion


SCHEDULE_ROW_WEEKDAY_KEYS = (
   'monday',
   'tuesday',
   'wednesday',
   'thursday',
   'friday',
   'saturday',
   'sunday',
)


@dataclass( frozen=True )
class ScheduleRowInput:
   time: str
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool

   @classmethod
   def from_wire( cls, row: Mapping[ str, Any ] ) -> Self | None:
      time = DateValues.normalize_schedule_time( row.get( 'time' ) )

      if time is None:
         return None

      return cls(
         time=time,
         **{
            day: ValueConversion.as_boolean( row.get( day ) )
            for day in SCHEDULE_ROW_WEEKDAY_KEYS
         } )


def parse_schedule_rows(
      schedule_rows: list[ dict[ str, Any ] ] | None ) -> list[ ScheduleRowInput ]:
   if not schedule_rows:
      return []

   parsed_rows: list[ ScheduleRowInput ] = []
   seen_seconds: set[ int ] = set()

   for row in schedule_rows:
      if not isinstance( row, dict ):
         continue

      parsed_row = ScheduleRowInput.from_wire( row )

      if parsed_row is None:
         continue

      time_seconds = DateValues.time_value_in_seconds( parsed_row.time )

      if time_seconds is None or time_seconds in seen_seconds:
         continue

      seen_seconds.add( time_seconds )
      parsed_rows.append( parsed_row )

   return parsed_rows
