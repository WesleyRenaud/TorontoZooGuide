from __future__ import annotations

from ..types import Types


class DateRange:
   def __init__( self, start_date: Types.DateKey, end_date: Types.DateKey ) -> None:
      self.start_date = start_date
      self.end_date = end_date
