from __future__ import annotations

from dataclasses import dataclass

from .itinerary_name_key import itinerary_name_key
from ...types import ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryGuardiansTalkRecord:
   talk_name: str
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey
   is_deleted: bool


   def name_key( self ) -> str:
      return itinerary_name_key( self.talk_name )
