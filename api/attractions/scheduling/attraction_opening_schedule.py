from __future__ import annotations

from ...types import Types


class AttractionOpeningSchedule:
   def __init__(
         self,
         attraction: str,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str | None ) -> None:
      self.attraction = attraction
      self.start_date = start_date
      self.end_date = end_date
      self.monday = monday
      self.tuesday = tuesday
      self.wednesday = wednesday
      self.thursday = thursday
      self.friday = friday
      self.saturday = saturday
      self.sunday = sunday
      self.holidays_only = holidays_only
      self.message = message
