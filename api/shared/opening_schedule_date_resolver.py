from __future__ import annotations

from datetime import date

from .calendar_dates import DateValues
from ..types import Types


class OpeningScheduleDateResolver():
   @classmethod
   def parse_end_date(
         cls,
         value: Types.DateInput ) -> date:
      if value == None:
         return date.max

      return DateValues.parse_date_value( value )


   @classmethod
   def format_date(
         cls,
         value: date ) -> Types.DateKey | None:
      if value == date.max:
         return None

      return value.isoformat()
