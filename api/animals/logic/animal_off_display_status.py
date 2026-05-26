from __future__ import annotations

from ...shared.enums import AnimalViewingScope
from ...types import DateKey


class AnimalOffDisplayStatus:
   def __init__(
         self,
         species: str,
         exhibit: str,
         viewing_scope: AnimalViewingScope,
         start_date: DateKey,
         end_date: DateKey,
         message: str ) -> None:
      self.species = species
      self.exhibit = exhibit
      self.viewing_scope = viewing_scope
      self.start_date = start_date
      self.end_date = end_date
      self.message = message
