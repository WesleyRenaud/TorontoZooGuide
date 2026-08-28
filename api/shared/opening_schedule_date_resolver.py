from __future__ import annotations

from datetime import date

from .calendar_dates import DateValues
from ..types import DateInput, DateKey


class OpeningScheduleDateResolver():
   @classmethod
   def parse_end_date(
         cls,
         value: DateInput ) -> date:
      if value == None:
         return date.max

      return DateValues.parse_date_value( value )


   @classmethod
   def format_date(
         cls,
         value: date ) -> DateKey | None:
      if value == date.max:
         return None

      return value.isoformat()
