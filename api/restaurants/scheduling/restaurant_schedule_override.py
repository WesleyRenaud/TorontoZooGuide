from __future__ import annotations

from ...types import DateKey


class RestaurantScheduleOverride:
   def __init__(
         self,
         restaurant: str,
         start_date: DateKey,
         end_date: DateKey | None,
         is_closed: bool,
         message: str | None ) -> None:
      self.restaurant = restaurant
      self.start_date = start_date
      self.end_date = end_date
      self.is_closed = is_closed
      self.message = message
