from __future__ import annotations

from ...types import DateKey


class UpdateEndInput:
   def __init__(
         self,
         title: str,
         start_date: DateKey,
         end_date: DateKey ) -> None:
      self.title = title
      self.start_date = start_date
      self.end_date = end_date
