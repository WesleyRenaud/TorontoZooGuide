from __future__ import annotations

from ...types import DateKey


class UpdateCreateInput:
   def __init__(
         self,
         title: str,
         description: str,
         update_type: str,
         start_date: DateKey,
         end_date: DateKey | None ) -> None:
      self.title = title
      self.description = description
      self.update_type = update_type
      self.start_date = start_date
      self.end_date = end_date
