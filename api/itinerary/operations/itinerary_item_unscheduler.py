from __future__ import annotations

from ..animal_schedule_item_key import AnimalScheduleItemKey
from ..attraction_schedule_item_key import AttractionScheduleItemKey
from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ..data_access.saved_itinerary_schedule_item_row_finder import SavedItineraryScheduleItemRowFinder
from ..data_access.unschedule_itinerary_item_provider import UnscheduleItineraryItemProvider
from ..guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from .itinerary_item_schedule_change_committer import ItineraryItemScheduleChangeCommitter
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.items.schedule_item_key import ScheduleItemKey
from ...shared.enums import ItineraryEventType
from ..transportation_schedule_item_key import TransportationScheduleItemKey
from ...types import Types
from ..wild_encounter_schedule_item_key import WildEncounterScheduleItemKey


class ItineraryItemUnscheduler():
   @classmethod
   def apply(
         cls,
         cur: Types.Cursor,
         schedule_item_key: ScheduleItemKey.Key ) -> None:
      if isinstance( schedule_item_key, AnimalScheduleItemKey ):
         UnscheduleItineraryItemProvider.clear_itinerary_animal_schedule(
            cur,
            species=schedule_item_key.species,
            exhibit=schedule_item_key.exhibit,
            enclosure_name=schedule_item_key.enclosure_name )
         return

      if isinstance( schedule_item_key, TransportationScheduleItemKey ):
         UnscheduleItineraryItemProvider.clear_itinerary_transportation_schedule(
            cur,
            name=schedule_item_key.name,
            added_as_attraction=schedule_item_key.added_as_attraction )
         return

      if isinstance( schedule_item_key, AttractionScheduleItemKey ):
         saved_row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
            ItineraryProvider.fetch_saved_itinerary( cur.connection ),
            schedule_item_key )

         if isinstance( saved_row, ItineraryTransportationRecord ):
            UnscheduleItineraryItemProvider.clear_itinerary_transportation_schedule(
               cur,
               name=schedule_item_key.name,
               added_as_attraction=saved_row.added_as_attraction )
            return

         UnscheduleItineraryItemProvider.clear_itinerary_attraction_schedule(
            cur,
            name=schedule_item_key.name )
         return

      if isinstance( schedule_item_key, GuardiansTalkScheduleItemKey ):
         UnscheduleItineraryItemProvider.clear_itinerary_guardians_talk_schedule(
            cur,
            talk_name=schedule_item_key.name )
         return

      if isinstance( schedule_item_key, WildEncounterScheduleItemKey ):
         UnscheduleItineraryItemProvider.clear_itinerary_wild_encounter_schedule(
            cur,
            wild_encounter=schedule_item_key.name )
         return

      if isinstance( schedule_item_key, ItineraryEventType ):
         UnscheduleItineraryItemProvider.delete_itinerary_event_schedule(
            cur,
            event_type=schedule_item_key )


   @classmethod
   def unschedule(
         cls,
         conn: Types.Connection,
         schedule_item_key: ScheduleItemKey.Key | None ) -> ItinerarySaveResult:
      return ItineraryItemScheduleChangeCommitter.commit(
         conn,
         schedule_item_key,
         cls.apply )
