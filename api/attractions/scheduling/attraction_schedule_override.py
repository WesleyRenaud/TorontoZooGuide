from __future__ import annotations

from ...types import Types


class AttractionScheduleOverride:
   def __init__(
         self,
         attraction: str,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None,
         is_closed: bool,
         message: str | None ) -> None:
      self.attraction = attraction
      self.start_date = start_date
      self.end_date = end_date
      self.is_closed = is_closed
      self.message = message
