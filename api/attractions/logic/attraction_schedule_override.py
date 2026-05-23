from __future__ import annotations

from ...types import DateKey


class AttractionScheduleOverride:
   def __init__(
         self,
         attraction: str,
         start_date: DateKey,
         end_date: DateKey | None,
         is_closed: bool,
         message: str | None ) -> None:
      self.attraction = attraction
      self.start_date = start_date
      self.end_date = end_date
      self.is_closed = is_closed
      self.message = message
