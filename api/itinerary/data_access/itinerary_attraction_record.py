from __future__ import annotations

from dataclasses import dataclass

from .itinerary_name_key import itinerary_name_key


@dataclass( frozen=True )
class ItineraryAttractionRecord:
   attraction: str
   old_likelihood: int | None
   new_likelihood: int | None


   def name_key( self ) -> str:
      return itinerary_name_key( self.attraction )
