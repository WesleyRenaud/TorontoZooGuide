from __future__ import annotations

from ...types import Types


class ExhibitClosedStatus:
   def __init__(
         self,
         exhibit: str,
         start_date: Types.DateKey,
         end_date: Types.DateKey,
         message: str ) -> None:
      self.exhibit = exhibit
      self.start_date = start_date
      self.end_date = end_date
      self.message = message
