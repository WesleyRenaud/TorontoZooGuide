from __future__ import annotations

from datetime import date

from .date_values import DateValues
from ..types import DateInput, DateKey


def parse_opening_schedule_end_date( value: DateInput ) -> date:
   if value == None:
      return date.max

   return DateValues.parse_date_value( value )


def format_opening_schedule_date( value: date ) -> DateKey | None:
   if value == date.max:
      return None

   return value.isoformat()
