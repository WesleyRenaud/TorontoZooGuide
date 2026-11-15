from __future__ import annotations

from datetime import date


class StationClosure():
   station: str
   message: str
   start: date | None
   end: date | None


   def __init__(
         self,
         station: str,
         message: str,
         start: date | None,
         end: date | None ) -> None:
      self.station = station
      self.message = message
      self.start = start
      self.end = end


   def dated( self ) -> bool:
      return self.start != None and self.end != None
