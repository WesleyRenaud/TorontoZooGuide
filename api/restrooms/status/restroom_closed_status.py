from __future__ import annotations

from ...types import DateKey


class RestroomClosedStatus:
   def __init__(
         self,
         restroom: str,
         start_date: DateKey,
         end_date: DateKey | None,
         message: str ) -> None:
      self.restroom = restroom
      self.start_date = start_date
      self.end_date = end_date
      self.message = message
