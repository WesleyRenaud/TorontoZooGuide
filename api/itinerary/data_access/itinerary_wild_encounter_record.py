from __future__ import annotations

from dataclasses import dataclass

from ...app_strings import format_app_string
from .itinerary_name_key import itinerary_name_key
from ...types import ScheduleTimeKey
from ..wild_encounter_item_key import WildEncounterScheduleItemKey


@dataclass( frozen=True )
class ItineraryWildEncounterRecord:
   wild_encounter: str
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey
   is_deleted: bool


   def name_key( self ) -> str:
      return itinerary_name_key( self.wild_encounter )


   def schedule_item_key( self ) -> WildEncounterScheduleItemKey:
      key = WildEncounterScheduleItemKey.from_row( self )

      if key is None:
         raise ValueError(
            format_app_string(
               'guestStatus.itinerary.wildEncounterRowMissingStartTime',
               wildEncounter=repr( self.wild_encounter ) ) )

      return key
