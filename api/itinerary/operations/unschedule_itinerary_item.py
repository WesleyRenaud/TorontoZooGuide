from __future__ import annotations

from ..animal_item_key import AnimalScheduleItemKey
from ..attraction_item_key import AttractionScheduleItemKey
from .commit_itinerary_item_schedule_change import commit_itinerary_item_schedule_change
from ..data_access.attraction_also_transportation import attraction_is_also_transportation
from ..data_access.unschedule_itinerary_item import clear_itinerary_animal_schedule
from ..data_access.unschedule_itinerary_item import clear_itinerary_attraction_schedule
from ..data_access.unschedule_itinerary_item import clear_itinerary_guardians_talk_schedule
from ..data_access.unschedule_itinerary_item import clear_itinerary_transportation_schedule
from ..data_access.unschedule_itinerary_item import clear_itinerary_wild_encounter_schedule
from ..data_access.unschedule_itinerary_item import delete_itinerary_event_schedule
from ..guardians_talk_item_key import GuardiansTalkScheduleItemKey
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.items.schedule_item_key import ScheduleItemKey
from ...shared.enums import ItineraryEventType
from ...types import Connection
from ...types import Cursor
from ..wild_encounter_item_key import WildEncounterScheduleItemKey


def _apply_unschedule(
      cur: Cursor,
      schedule_item_key: ScheduleItemKey ) -> None:
   if isinstance( schedule_item_key, AnimalScheduleItemKey ):
      clear_itinerary_animal_schedule(
         cur,
         species=schedule_item_key.species,
         exhibit=schedule_item_key.exhibit,
         enclosure_name=schedule_item_key.enclosure_name )
      return

   if isinstance( schedule_item_key, AttractionScheduleItemKey ):
      if attraction_is_also_transportation(
            cur.connection,
            schedule_item_key.name ):
         clear_itinerary_transportation_schedule(
            cur,
            name=schedule_item_key.name )
         return

      clear_itinerary_attraction_schedule(
         cur,
         name=schedule_item_key.name )
      return

   if isinstance( schedule_item_key, GuardiansTalkScheduleItemKey ):
      clear_itinerary_guardians_talk_schedule(
         cur,
         talk_name=schedule_item_key.name )
      return

   if isinstance( schedule_item_key, WildEncounterScheduleItemKey ):
      clear_itinerary_wild_encounter_schedule(
         cur,
         wild_encounter=schedule_item_key.name )
      return

   if isinstance( schedule_item_key, ItineraryEventType ):
      delete_itinerary_event_schedule( cur, event_type=schedule_item_key )


def unschedule_itinerary_item(
      conn: Connection,
      schedule_item_key: ScheduleItemKey | None ) -> ItinerarySaveResult:
   return commit_itinerary_item_schedule_change(
      conn,
      schedule_item_key,
      _apply_unschedule )
