from __future__ import annotations

from ..animal_item_key import AnimalScheduleItemKey
from ..attraction_item_key import AttractionScheduleItemKey
from .commit_itinerary_item_schedule_change import commit_itinerary_item_schedule_change
from ..data_access.find_saved_itinerary_schedule_item_row import find_saved_itinerary_schedule_item_row
from ..data_access.itinerary import fetch_saved_itinerary
from ..data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ..data_access.remove_itinerary_item import delete_itinerary_animal
from ..data_access.remove_itinerary_item import delete_itinerary_attraction
from ..data_access.remove_itinerary_item import delete_itinerary_event
from ..data_access.remove_itinerary_item import delete_itinerary_guardians_talk
from ..data_access.remove_itinerary_item import delete_itinerary_transportation
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
      saved_row = find_saved_itinerary_schedule_item_row(
         fetch_saved_itinerary( cur.connection ),
         schedule_item_key )

      if isinstance( saved_row, ItineraryTransportationRecord ):
         delete_itinerary_transportation(
            cur,
            name=schedule_item_key.name,
            added_as_attraction=saved_row.added_as_attraction )
         return

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
