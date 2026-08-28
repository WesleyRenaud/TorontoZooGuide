from __future__ import annotations

from ...shared.enums import AnimalViewingScope
from ...types import Types


class AnimalOffDisplayStatus:
   def __init__(
         self,
         species: str,
         exhibit: str,
         viewing_scope: AnimalViewingScope,
         start_date: Types.DateKey,
         end_date: Types.DateKey,
         message: str ) -> None:
      self.species = species
      self.exhibit = exhibit
      self.viewing_scope = viewing_scope
      self.start_date = start_date
      self.end_date = end_date
      self.message = message
