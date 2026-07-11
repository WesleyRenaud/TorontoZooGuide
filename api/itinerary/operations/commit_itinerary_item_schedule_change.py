from __future__ import annotations

from collections.abc import Callable

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.itinerary import fetch_saved_itinerary
from ..domain.itinerary import build_current_itinerary
from ..domain.itinerary_adjustment import ItineraryAdjustment
from ...guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ..results.itinerary_save_result import ItinerarySaveResult
from ..scheduling.items.schedule_item_key import ScheduleItemKey
from ..scheduling.items.schedule_itinerary_helpers import build_itinerary_context
from ..scheduling.items.schedule_itinerary_helpers import build_success_result
from ..scheduling.items.schedule_itinerary_helpers import persist_itinerary_walk_route
from ..scheduling.unscheduling.shift_guest_schedules_after_unschedule import apply_guest_schedule_shift_for_unschedule
from ..scheduling.unscheduling.shift_guest_schedules_after_unschedule import resolve_unscheduled_item_time_block
from ..scheduling.unscheduling.update_visit_times_after_schedule_item_removed import update_arrival_to_earliest_scheduled_start
from ..scheduling.unscheduling.update_visit_times_after_schedule_item_removed import update_departure_to_latest_scheduled_end
from ..scheduling.unscheduling.update_visit_times_after_schedule_item_removed import was_first_scheduled_item
from ..scheduling.unscheduling.update_visit_times_after_schedule_item_removed import was_last_scheduled_item
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

   saved_itinerary = fetch_saved_itinerary( conn )
   itinerary_before = build_current_itinerary(
      saved_itinerary,
      **itinerary_context )
   removed_block = (
      resolve_unscheduled_item_time_block(
         saved_itinerary,
         schedule_item_key )
      if schedule_item_key is not None
      else None )
   removed_first_item = was_first_scheduled_item(
      itinerary_before,
      removed_block )
   removed_last_item = was_last_scheduled_item(
      itinerary_before,
      removed_block )
   cur = conn.cursor()

   try:
      if schedule_item_key is not None:
         apply_guest_schedule_shift_for_unschedule(
            conn,
            cur,
            saved_itinerary=saved_itinerary,
            schedule_item_key=schedule_item_key )
         apply_change( cur, schedule_item_key )

      conn.commit()

   finally:
      cur.close()

   itinerary_after = build_current_itinerary(
      fetch_saved_itinerary( conn ),
      **itinerary_context )
   adjustments: list[ ItineraryAdjustment ] = []

   if removed_first_item:
      arrival_adjustment = update_arrival_to_earliest_scheduled_start(
         conn,
         itinerary_after,
         previous_arrival_time=itinerary_before.arrival_time )

      if arrival_adjustment is not None:
         adjustments.append( arrival_adjustment )

   if removed_last_item:
      departure_adjustment = update_departure_to_latest_scheduled_end(
         conn,
         itinerary_after,
         previous_departure_time=itinerary_before.departure_time )

      if departure_adjustment is not None:
         adjustments.append( departure_adjustment )

   persist_itinerary_walk_route( conn, **itinerary_context )

   return build_success_result(
      conn,
      adjustments=tuple( adjustments ),
      **itinerary_context )
