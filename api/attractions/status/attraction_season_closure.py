from __future__ import annotations

from ...types import Types


class AttractionSeasonClosure:
   def __init__(
         self,
         attraction: str,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None,
         message: str,
         is_closed_for_season: bool ) -> None:
      self.attraction = attraction
      self.start_date = start_date
      self.end_date = end_date
      self.message = message
      self.is_closed_for_season = is_closed_for_season
