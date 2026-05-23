from __future__ import annotations

from ...types import DateKey


class AnimalViewingAlert:
   def __init__(
         self,
         species: str,
         exhibit: str,
         start_date: DateKey,
         end_date: DateKey,
         message: str ) -> None:
      self.species = species
      self.exhibit = exhibit
      self.start_date = start_date
      self.end_date = end_date
      self.message = message
