from __future__ import annotations

from ...types import Types


class RestroomAlert:
   def __init__(
         self,
         restroom: str,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None,
         message: str ) -> None:
      self.restroom = restroom
      self.start_date = start_date
      self.end_date = end_date
      self.message = message
