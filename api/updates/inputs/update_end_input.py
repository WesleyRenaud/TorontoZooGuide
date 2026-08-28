from __future__ import annotations

from ...types import Types


class UpdateEndInput:
   def __init__(
         self,
         title: str,
         start_date: Types.DateKey,
         end_date: Types.DateKey ) -> None:
      self.title = title
      self.start_date = start_date
      self.end_date = end_date
