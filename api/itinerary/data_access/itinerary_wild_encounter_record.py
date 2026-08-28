from __future__ import annotations

from dataclasses import dataclass

from ...app_strings import AppStringProvider
from .itinerary_name_key_builder import ItineraryNameKeyBuilder
from ...types import ScheduleTimeKey
from ..wild_encounter_item_key import WildEncounterScheduleItemKey


@dataclass( frozen=True )
class ItineraryWildEncounterRecord:
   wild_encounter: str
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey
   is_deleted: bool


   def name_key( self ) -> str:
      return ItineraryNameKeyBuilder.build( self.wild_encounter )


   def schedule_item_key( self ) -> WildEncounterScheduleItemKey:
      key = WildEncounterScheduleItemKey.from_row( self )

      if key is None:
         raise ValueError(
            AppStringProvider.format(
               'guestStatus.itinerary.wildEncounterRowMissingStartTime',
               wildEncounter=repr( self.wild_encounter ) ) )

      return key
