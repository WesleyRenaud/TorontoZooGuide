from __future__ import annotations

from ..animal_item_key import AnimalScheduleItemKey
from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ..attraction_item_key import AttractionScheduleItemKey
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from .commit_itinerary_item_schedule_change import commit_itinerary_item_schedule_change
from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ..data_access.remove_itinerary_item_provider import RemoveItineraryItemProvider
from ..data_access.saved_itinerary_schedule_item_row_finder import SavedItineraryScheduleItemRowFinder
from ..domain.itinerary_builder import ItineraryBuilder
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ..guardians_talk_item_key import GuardiansTalkScheduleItemKey
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.bulk.bulk_schedule_itinerary_runner import BulkScheduleItineraryRunner
from ..scheduling.bulk.bulk_schedule_stop_selector import BulkScheduleStopSelector
from ..scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from ..scheduling.items.itinerary_schedule_context_builder import ItineraryScheduleContextBuilder
from ..scheduling.items.schedule_item_key import ScheduleItemKey
from ..scheduling.scheduled_endpoint_visit_times_syncer import ScheduledEndpointVisitTimesSyncer
from ...shared.enums import ItineraryEventType
from ..transportation_item_key import TransportationScheduleItemKey
from ...types import Connection
from ...types import Cursor
from ..wild_encounter_item_key import WildEncounterScheduleItemKey
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def _is_transit_mode_transportation_key(
      schedule_item_key: ScheduleItemKey | None ) -> bool:
   return (
      isinstance( schedule_item_key, TransportationScheduleItemKey )
      and not schedule_item_key.added_as_attraction
   )


def _apply_remove(
      cur: Cursor,
      schedule_item_key: ScheduleItemKey ) -> None:
   if isinstance( schedule_item_key, AnimalScheduleItemKey ):
      RemoveItineraryItemProvider.delete_itinerary_animal(
         cur,
         species=schedule_item_key.species,
         exhibit=schedule_item_key.exhibit,
         enclosure_name=schedule_item_key.enclosure_name )
      return

   if isinstance( schedule_item_key, TransportationScheduleItemKey ):
      RemoveItineraryItemProvider.delete_itinerary_transportation(
         cur,
         name=schedule_item_key.name,
         added_as_attraction=schedule_item_key.added_as_attraction )
      return

   if isinstance( schedule_item_key, AttractionScheduleItemKey ):
      saved_row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
         ItineraryProvider.fetch_saved_itinerary( cur.connection ),
         schedule_item_key )

      if isinstance( saved_row, ItineraryTransportationRecord ):
         RemoveItineraryItemProvider.delete_itinerary_transportation(
            cur,
            name=schedule_item_key.name,
            added_as_attraction=saved_row.added_as_attraction )
         return

      RemoveItineraryItemProvider.delete_itinerary_attraction(
         cur,
         name=schedule_item_key.name )
      return

   if isinstance( schedule_item_key, GuardiansTalkScheduleItemKey ):
      RemoveItineraryItemProvider.delete_itinerary_guardians_talk(
         cur,
         talk_name=schedule_item_key.name )
      return

   if isinstance( schedule_item_key, WildEncounterScheduleItemKey ):
      RemoveItineraryItemProvider.delete_itinerary_wild_encounter(
         cur,
         wild_encounter=schedule_item_key.name )
      return

   if isinstance( schedule_item_key, ItineraryEventType ):
      RemoveItineraryItemProvider.delete_itinerary_event( cur, event_type=schedule_item_key )


def _remove_transit_transportation_and_reschedule(
      conn: Connection,
      schedule_item_key: TransportationScheduleItemKey,
) -> ItinerarySaveResult:
   itinerary_context = ItineraryScheduleContextBuilder.build(
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )
   saved_before = ItineraryProvider.fetch_saved_itinerary( conn )
   itinerary_before = ItineraryBuilder.build_current(
      saved_before,
      **itinerary_context )
   cur = conn.cursor()

   try:
      _apply_remove( cur, schedule_item_key )
      conn.commit()
   finally:
      cur.close()

   saved_after = ItineraryProvider.fetch_saved_itinerary( conn )
   stops_to_schedule = BulkScheduleStopSelector.stops_matching_previous(
      saved_before,
      saved_after )

   if stops_to_schedule:
      return BulkScheduleItineraryRunner.run(
         conn,
         stops_to_schedule=stops_to_schedule,
         confirming_fixed_time_item_long_wait=True,
         **itinerary_context )

   ScheduledEndpointVisitTimesSyncer.sync_if_complete(
      conn,
      ItineraryBuilder.build_current(
         saved_after,
         **itinerary_context ) )
   ScheduledEndpointVisitTimesSyncer.clear_if_became_incomplete(
      conn,
      previous_itinerary=itinerary_before,
      current_itinerary=ItineraryBuilder.build_current(
         ItineraryProvider.fetch_saved_itinerary( conn ),
         **itinerary_context ) )
   ItinerarySaveResultBuilder.persist_walk_route( conn, **itinerary_context )

   return ItinerarySaveResultBuilder.success_result( conn, **itinerary_context )


def remove_itinerary_item(
      conn: Connection,
      schedule_item_key: ScheduleItemKey | None ) -> ItinerarySaveResult:
   if _is_transit_mode_transportation_key( schedule_item_key ):
      assert isinstance( schedule_item_key, TransportationScheduleItemKey )
      return _remove_transit_transportation_and_reschedule(
         conn,
         schedule_item_key )

   return commit_itinerary_item_schedule_change(
      conn,
      schedule_item_key,
      _apply_remove )
