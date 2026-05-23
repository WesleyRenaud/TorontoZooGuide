from __future__ import annotations

from ...types import DateKey


class AnimalLimitedViewingSchedule:
   def __init__(
         self,
         species: str,
         exhibit: str,
         start_date: DateKey,
         end_date: DateKey,
         daily_start_time: str,
         daily_end_time: str,
         message: str ) -> None:
      self.species = species
      self.exhibit = exhibit
      self.start_date = start_date
      self.end_date = end_date
      self.daily_start_time = daily_start_time
      self.daily_end_time = daily_end_time
      self.message = message
