from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from .itinerary_animal_input import ItineraryAnimalInput
from .itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from ...types import ScheduleTimeKey
from ..wild_encounter_item_key import WildEncounterScheduleItemKey


@dataclass( frozen=True )
class ItinerarySaveInput:
   date: date
   arrival_time: ScheduleTimeKey
   departure_time: ScheduleTimeKey
   animals: list[ ItineraryAnimalInput ]
   attractions: list[ str ]
   guardians_talks: list[ ItineraryGuardiansTalkInput ]
   wild_encounters: list[ WildEncounterScheduleItemKey ]
   selected_exhibits: list[ str ] = field( default_factory=list )


   def month( self ) -> int:
      return self.date.month


   def day( self ) -> int:
      return self.date.day


   def year( self ) -> int:
      return self.date.year
