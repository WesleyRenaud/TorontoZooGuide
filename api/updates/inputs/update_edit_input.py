from __future__ import annotations

from ...types import Types


class UpdateEditInput:
   def __init__(
         self,
         title: str,
         start_date: Types.DateKey,
         description: str,
         update_type: str,
         end_date: Types.DateKey | None ) -> None:
      self.title = title
      self.start_date = start_date
      self.description = description
      self.update_type = update_type
      self.end_date = end_date
