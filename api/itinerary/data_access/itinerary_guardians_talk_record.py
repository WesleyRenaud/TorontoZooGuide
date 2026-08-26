from __future__ import annotations

from dataclasses import dataclass

from .itinerary_name_key_builder import ItineraryNameKeyBuilder
from ...types import ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryGuardiansTalkRecord:
   talk_name: str
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey
   is_deleted: bool


   def name_key( self ) -> str:
      return ItineraryNameKeyBuilder.build( self.talk_name )
