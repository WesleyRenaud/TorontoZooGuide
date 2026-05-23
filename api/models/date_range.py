from __future__ import annotations

from ..types import DateKey


class DateRange:
   def __init__( self, start_date: DateKey, end_date: DateKey ) -> None:
      self.start_date = start_date
      self.end_date = end_date
