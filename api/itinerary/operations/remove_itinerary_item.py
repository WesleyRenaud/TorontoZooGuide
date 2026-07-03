from __future__ import annotations

from ..animal_item_key import AnimalScheduleItemKey
from ..attraction_item_key import AttractionScheduleItemKey
from .commit_itinerary_item_schedule_change import commit_itinerary_item_schedule_change
from ..data_access.remove_itinerary_item import delete_itinerary_animal
from ..data_access.remove_itinerary_item import delete_itinerary_attraction
from ..data_access.remove_itinerary_item import delete_itinerary_event
from ..data_access.remove_itinerary_item import delete_itinerary_guardians_talk
from ..data_access.remove_itinerary_item import delete_itinerary_wild_encounter
from ..guardians_talk_item_key import GuardiansTalkScheduleItemKey
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.items.schedule_item_key import ScheduleItemKey
from ...shared.enums import ItineraryEventType
from ...types import Connection
from ...types import Cursor
from ..wild_encounter_item_key import WildEncounterScheduleItemKey


def _apply_remove(
      cur: Cursor,
      schedule_item_key: ScheduleItemKey ) -> None:
   if isinstance( schedule_item_key, AnimalScheduleItemKey ):
      delete_itinerary_animal(
         cur,
         species=schedule_item_key.species,
         exhibit=schedule_item_key.exhibit,
         enclosure_name=schedule_item_key.enclosure_name )
      return

   if isinstance( schedule_item_key, AttractionScheduleItemKey ):
      delete_itinerary_attraction(
         cur,
         name=schedule_item_key.name )
      return

   if isinstance( schedule_item_key, GuardiansTalkScheduleItemKey ):
      delete_itinerary_guardians_talk(
         cur,
         talk_name=schedule_item_key.name )
      return

   if isinstance( schedule_item_key, WildEncounterScheduleItemKey ):
      delete_itinerary_wild_encounter(
         cur,
         wild_encounter=schedule_item_key.name )
      return

   if isinstance( schedule_item_key, ItineraryEventType ):
      delete_itinerary_event( cur, event_type=schedule_item_key )


def remove_itinerary_item(
      conn: Connection,
      schedule_item_key: ScheduleItemKey | None ) -> ItinerarySaveResult:
   return commit_itinerary_item_schedule_change(
      conn,
      schedule_item_key,
      _apply_remove )
