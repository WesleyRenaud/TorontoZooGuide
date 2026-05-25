from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .itinerary_animal_input import ItineraryAnimalInput
from .itinerary_guardians_talk_input import ItineraryGuardiansTalkInput


@dataclass( frozen=True )
class ItinerarySaveInput:
   date: date
   animals: tuple[ ItineraryAnimalInput, ... ]
   attractions: tuple[ str, ... ]
   guardians_talks: tuple[ ItineraryGuardiansTalkInput, ... ]
   wild_encounters: tuple[ str, ... ]
   selected_exhibits: tuple[ str, ... ] = ()


   def month( self ) -> int:
      return self.date.month


   def day( self ) -> int:
      return self.date.day


   def year( self ) -> int:
      return self.date.year
