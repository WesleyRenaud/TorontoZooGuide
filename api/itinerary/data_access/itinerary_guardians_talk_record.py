from __future__ import annotations

from dataclasses import dataclass

from .itinerary_name_key_builder import ItineraryNameKeyBuilder
from ...types import Types


@dataclass( frozen=True )
class ItineraryGuardiansTalkRecord:
   talk_name: str
   start_time: Types.ScheduleTimeKey
   end_time: Types.ScheduleTimeKey
   is_deleted: bool


   def name_key( self ) -> str:
      return ItineraryNameKeyBuilder.build( self.talk_name )
