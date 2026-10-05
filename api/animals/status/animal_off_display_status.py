from __future__ import annotations

from ..domain.animal_viewing_scope import AnimalViewingScope
from ...types import Types


class AnimalOffDisplayStatus:
   def __init__(
         self,
         species: str,
         exhibit: str,
         viewing_scopes: list[ AnimalViewingScope ],
         start_date: Types.DateKey,
         end_date: Types.DateKey,
         message: str,
         is_off_display_for_season: bool ) -> None:
      self.species = species
      self.exhibit = exhibit
      self.viewing_scopes = viewing_scopes
      self.start_date = start_date
      self.end_date = end_date
      self.message = message
      self.is_off_display_for_season = is_off_display_for_season
