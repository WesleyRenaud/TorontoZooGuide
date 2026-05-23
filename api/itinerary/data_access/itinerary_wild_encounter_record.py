from __future__ import annotations

from dataclasses import dataclass

from ...types import ScheduleTimeKey
from .itinerary_name_key import itinerary_name_key


@dataclass( frozen=True )
class ItineraryWildEncounterRecord:
   wild_encounter: str
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey
   is_deleted: bool


   def name_key( self ) -> str:
      return itinerary_name_key( self.wild_encounter )
