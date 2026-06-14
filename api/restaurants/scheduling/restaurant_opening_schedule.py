from __future__ import annotations

from ...types import DateKey


class RestaurantOpeningSchedule:
   def __init__(
         self,
         restaurant: str,
         start_date: DateKey,
         end_date: DateKey | None,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str | None ) -> None:
      self.restaurant = restaurant
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
