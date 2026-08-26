from __future__ import annotations

from collections.abc import Callable

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ..attraction_item_key import AttractionScheduleItemKey
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.itinerary_provider import ItineraryProvider
from ..domain.itinerary_builder import ItineraryBuilder
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ..guardians_talk_item_key import GuardiansTalkScheduleItemKey
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.bulk.attraction_covered_animals import restore_covered_animals_after_attraction_removed
from ..scheduling.bulk.guardians_talk_covered_animals import restore_covered_animals_after_talk_removed
from ..scheduling.items.schedule_item_key import ScheduleItemKey
from ..scheduling.items.schedule_itinerary_helpers import build_itinerary_context
from ..scheduling.items.schedule_itinerary_helpers import build_success_result
from ..scheduling.items.schedule_itinerary_helpers import persist_itinerary_walk_route
from ..scheduling.sync_visit_times_to_scheduled_endpoints import clear_visit_times_if_became_incomplete
from ..scheduling.sync_visit_times_to_scheduled_endpoints import sync_visit_times_to_scheduled_endpoints_if_complete
from ..scheduling.unscheduling.shift_guest_schedules_after_unschedule import apply_guest_schedule_shift_for_unschedule
from ..scheduling.unscheduling.shift_guest_schedules_after_unschedule import resolve_unscheduled_item_time_block
from ..scheduling.unscheduling.shift_guest_schedules_after_unschedule import shift_guest_scheduled_items_after_unschedule
from ...types import Connection
from ...types import Cursor
from ...wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def commit_itinerary_item_schedule_change(
      conn: Connection,
      schedule_item_key: ScheduleItemKey | None,
      apply_change: Callable[ [ Cursor, ScheduleItemKey ], None ],
      ) -> ItinerarySaveResult:
   itinerary_context = build_itinerary_context(
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )
   itinerary_before = ItineraryBuilder.build_current(
      saved_itinerary,
      **itinerary_context )
   removed_block = (
      resolve_unscheduled_item_time_block(
         saved_itinerary,
         schedule_item_key )
      if schedule_item_key is not None
      else None )
   restored_covered_animals = None
   cur = conn.cursor()

   try:
      if schedule_item_key is not None:
         if (
               isinstance( schedule_item_key, GuardiansTalkScheduleItemKey )
               and removed_block is not None ):
            restored_covered_animals = restore_covered_animals_after_talk_removed(
               cur,
               conn,
               talk_name=schedule_item_key.name,
               talk_block=removed_block,
               animal_rows=saved_itinerary.animal_rows )
         elif (
               isinstance( schedule_item_key, AttractionScheduleItemKey )
               and removed_block is not None ):
            restored_covered_animals = restore_covered_animals_after_attraction_removed(
               cur,
               conn,
               attraction_name=schedule_item_key.name,
               attraction_block=removed_block,
               animal_rows=saved_itinerary.animal_rows )

         if (
               restored_covered_animals is not None
               and restored_covered_animals.replacement_end_seconds is not None
               and removed_block is not None ):
            shift_guest_scheduled_items_after_unschedule(
               conn,
               cur,
               anchor_end_seconds=removed_block.end_seconds,
               shift_seconds=(
                  restored_covered_animals.replacement_end_seconds
                  - removed_block.end_seconds ),
               freed_block=removed_block )
         else:
            apply_guest_schedule_shift_for_unschedule(
               conn,
               cur,
               saved_itinerary=saved_itinerary,
               schedule_item_key=schedule_item_key )

         apply_change( cur, schedule_item_key )

      conn.commit()

   finally:
      cur.close()

   itinerary_after = ItineraryBuilder.build_current(
      ItineraryProvider.fetch_saved_itinerary( conn ),
      **itinerary_context )
   sync_visit_times_to_scheduled_endpoints_if_complete(
      conn,
      itinerary_after )
   clear_visit_times_if_became_incomplete(
      conn,
      previous_itinerary=itinerary_before,
      current_itinerary=ItineraryBuilder.build_current(
         ItineraryProvider.fetch_saved_itinerary( conn ),
         **itinerary_context ) )

   persist_itinerary_walk_route( conn, **itinerary_context )

   return build_success_result(
      conn,
      adjustments=[],
      **itinerary_context )
