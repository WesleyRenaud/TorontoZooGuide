from __future__ import annotations

from ....animals.coordinators.animal_coordinator import AnimalCoordinator
from .attraction_covered_animals import apply_covered_by_attraction_schedules
from .attraction_covered_animals import merge_covered_viewing_spot_keys
from .attraction_covered_animals import viewing_spot_keys_to_cover_for_attractions
from ....attractions.coordinators.attraction_coordinator import AttractionCoordinator
from .bulk_schedule_arrival_adjustment import adjust_arrival_after_bulk_schedule
from .bulk_schedule_loop_pins import attach_loop_pins_to_schedule_windows
from .bulk_schedule_loop_pins import keep_completable_loop_pins
from .bulk_schedule_loop_pins import separate_schedule_boundaries_and_loop_pins
from .bulk_schedule_start_state import BulkScheduleStartState
from .bulk_schedule_walk_order import representative_walk_node_id
from ..core.guest_item_schedule_status import has_itinerary_schedule_times
from ..core.time_block import collect_time_blocks_from_itinerary
from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...domain.itinerary import build_current_itinerary
from ...domain.itinerary_adjustment import ItineraryAdjustment
from .group_stops_by_master_route_loop import group_stops_by_master_route_loop
from ....guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from .guardians_talk_covered_animals import apply_covered_by_talk_schedules
from .guardians_talk_covered_animals import filter_animals_excluding_covered
from .guardians_talk_covered_animals import viewing_spot_keys_to_cover_for_loop_pins
from ..items.schedule_itinerary_helpers import build_itinerary_context
from ..items.schedule_itinerary_helpers import build_save_result
from ..items.schedule_itinerary_helpers import persist_itinerary_walk_route
from ..items.schedule_itinerary_helpers import prepare_zoo_hours_schedule_window
from .loop_schedule_stop import animals_from_stops
from .loop_schedule_stop import attractions_from_stops
from .loop_schedule_stop import LoopScheduleStop
from .loop_schedule_unit import build_loop_schedule_units
from .restore_guest_schedule_state import restore_guest_schedule_state
from .restore_guest_schedule_state import snapshot_guest_schedule_state
from ...results.itinerary_result_reason import ItineraryResultReason
from ...results.itinerary_save_result import ItinerarySaveResult
from ...routing.partition_itinerary_schedule_windows import partition_itinerary_schedule_windows
from ...routing.resolve_itinerary_stops import resolve_fixed_time_itinerary_stops
from .schedule_animals_by_master_route_loop import schedule_animals_by_master_route_loop
from ....shared.calendar_dates import DateValues
from ....shared.enums import ItineraryErrorType
from ..sync_visit_times_to_scheduled_endpoints import clear_visit_times_if_became_incomplete
from ..sync_visit_times_to_scheduled_endpoints import sync_visit_times_to_scheduled_endpoints_if_complete
from ....types import Connection
from ..unscheduling.clear_all_itinerary_schedules import clear_all_itinerary_schedules
from ....walk_graph.data_access.load_walk_graph import load_walk_graph
from ....walk_graph.domain.walk_graph import WalkGraph
from ...warnings.bulk_schedule_animals_warning import build_bulk_schedule_animals_not_enough_time_issue
from ...warnings.fixed_time_item_long_wait_warning import fixed_time_item_long_wait_reasons_from_itinerary
from ....wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def is_itinerary_animal_unscheduled( animal_row: ItineraryAnimalRecord ) -> bool:
   return not has_itinerary_schedule_times(
      animal_row.start_time,
      animal_row.end_time )


def bulk_schedule_animals(
      conn: Connection,
      *,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      visit_date_temp: float | None = None,
      confirming_fixed_time_item_long_wait: bool = False,
      animals_to_schedule: list[ ItineraryAnimalRecord ] | None = None,
      stops_to_schedule: list[ LoopScheduleStop ] | None = None ) -> ItinerarySaveResult:
   itinerary_context = build_itinerary_context(
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_coordinator=guardians_coordinator,
      wild_encounter_coordinator=wild_encounter_coordinator,
      visit_date_temp=visit_date_temp )

   if stops_to_schedule is None:
      stops_to_schedule = list( animals_to_schedule or [] )

   if not stops_to_schedule:
      return build_save_result(
         conn,
         ItineraryErrorType.BULK_SCHEDULE_ANIMALS_ALREADY_SCHEDULED,
         **itinerary_context )

   saved_itinerary = fetch_saved_itinerary( conn )
   prepared_window = prepare_zoo_hours_schedule_window(
      conn,
      saved_itinerary,
      **itinerary_context )

   if isinstance( prepared_window, ItinerarySaveResult ):
      return prepared_window

   saved_itinerary = prepared_window.saved_itinerary
   schedule_snapshot, walk_route_snapshot = snapshot_guest_schedule_state(
      conn,
      saved_itinerary )

   previous_itinerary = build_current_itinerary(
      saved_itinerary,
      **itinerary_context )

   clear_all_itinerary_schedules( conn )

   saved_itinerary = fetch_saved_itinerary( conn )

   anchor_seconds, day_end_seconds = prepared_window.window
   itinerary = build_current_itinerary(
      saved_itinerary,
      **itinerary_context )
   blockers = collect_time_blocks_from_itinerary( itinerary )
   walk_graph = load_walk_graph()
   start_state = _bulk_schedule_start_state(
      walk_graph,
      saved_itinerary.animal_rows,
      anchor_seconds )

   fixed_time_stops = resolve_fixed_time_itinerary_stops( itinerary )
   boundary_stops, loop_pins = separate_schedule_boundaries_and_loop_pins(
      conn,
      itinerary,
      fixed_time_stops )
   schedule_windows = partition_itinerary_schedule_windows(
      start_state.schedule_anchor_seconds,
      day_end_seconds,
      boundary_stops )
   loop_pins = keep_completable_loop_pins( schedule_windows, loop_pins )
   animals_to_schedule = animals_from_stops( stops_to_schedule )
   attractions_to_pack = attractions_from_stops( stops_to_schedule )
   covered_by_talk = viewing_spot_keys_to_cover_for_loop_pins(
      conn,
      loop_pins,
      animals_to_schedule )
   covered_by_attraction = viewing_spot_keys_to_cover_for_attractions(
      conn,
      [
         attraction_row.attraction
         for attraction_row in attractions_to_pack
      ],
      animals_to_schedule )
   covered_keys = merge_covered_viewing_spot_keys(
      covered_by_talk,
      covered_by_attraction )
   animals_to_pack = filter_animals_excluding_covered(
      animals_to_schedule,
      covered_keys )
   stops_to_pack = [ *animals_to_pack, *attractions_to_pack ]
   sorted_loop_groups = group_stops_by_master_route_loop( stops_to_pack )
   loop_units = build_loop_schedule_units( sorted_loop_groups )
   schedule_windows = attach_loop_pins_to_schedule_windows(
      schedule_windows,
      loop_pins )

   if not loop_units and not covered_keys:
      itinerary = build_current_itinerary(
         fetch_saved_itinerary( conn ),
         **itinerary_context )
      sync_visit_times_to_scheduled_endpoints_if_complete( conn, itinerary )
      clear_visit_times_if_became_incomplete(
         conn,
         previous_itinerary=previous_itinerary,
         current_itinerary=build_current_itinerary(
            fetch_saved_itinerary( conn ),
            **itinerary_context ) )
      persist_itinerary_walk_route( conn, **itinerary_context )

      return ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         itinerary=build_current_itinerary(
            fetch_saved_itinerary( conn ),
            **itinerary_context ) )

   remaining_stops: list[ LoopScheduleStop ] = []

   if loop_units:
      remaining_stops, _ = schedule_animals_by_master_route_loop(
         conn,
         loop_units,
         blockers=blockers,
         schedule_windows=schedule_windows,
         schedule_cursor_seconds=start_state.schedule_anchor_seconds,
         walk_graph=walk_graph,
         start_node_id=start_state.start_node_id )

   apply_covered_by_talk_schedules( conn, covered_by_talk )
   apply_covered_by_attraction_schedules( conn, covered_by_attraction )

   adjustments: list[ ItineraryAdjustment ] = []
   reasons: list[ ItineraryResultReason ] = []

   if remaining_stops:
      reasons = [
         build_bulk_schedule_animals_not_enough_time_issue(
            remaining_stops ),
      ]
   else:
      itinerary_after_pack = build_current_itinerary(
         fetch_saved_itinerary( conn ),
         **itinerary_context )
      arrival_adjustment = adjust_arrival_after_bulk_schedule(
         conn,
         itinerary_after_pack,
         schedule_anchor_seconds=start_state.schedule_anchor_seconds,
         previous_arrival_time=schedule_snapshot.arrival_time )

      if arrival_adjustment is not None:
         adjustments = [ arrival_adjustment ]

      sync_visit_times_to_scheduled_endpoints_if_complete(
         conn,
         build_current_itinerary(
            fetch_saved_itinerary( conn ),
            **itinerary_context ) )

   clear_visit_times_if_became_incomplete(
      conn,
      previous_itinerary=previous_itinerary,
      current_itinerary=build_current_itinerary(
         fetch_saved_itinerary( conn ),
         **itinerary_context ) )

   persist_itinerary_walk_route( conn, **itinerary_context )

   itinerary = build_current_itinerary(
      fetch_saved_itinerary( conn ),
      **itinerary_context )
   pending_reasons = []

   if not confirming_fixed_time_item_long_wait:
      pending_reasons.extend(
         fixed_time_item_long_wait_reasons_from_itinerary( itinerary ) )

   if pending_reasons:
      restore_guest_schedule_state(
         conn,
         schedule_snapshot,
         walk_route_snapshot )

      return build_save_result(
         conn,
         pending_reasons[ 0 ].code,
         reasons=pending_reasons,
         **itinerary_context )

   return ItinerarySaveResult(
      status=ItineraryErrorType.SUCCESS,
      reasons=reasons,
      adjustments=adjustments,
      itinerary=itinerary )


def _bulk_schedule_start_state(
      walk_graph: WalkGraph,
      animal_rows: list[ ItineraryAnimalRecord ],
      anchor_seconds: int ) -> BulkScheduleStartState:
   entrance_node_id = str( walk_graph[ 'entrance_node_id' ] )
   scheduled_rows = [
      animal_row
      for animal_row in animal_rows
      if has_itinerary_schedule_times(
         animal_row.start_time,
         animal_row.end_time )
   ]

   if not scheduled_rows:
      return BulkScheduleStartState(
         start_node_id=entrance_node_id,
         schedule_anchor_seconds=anchor_seconds )

   last_scheduled_row = max(
      scheduled_rows,
      key=lambda animal_row: DateValues.time_value_in_seconds(
         animal_row.end_time ) or -1 )

   start_node_id = representative_walk_node_id(
      walk_graph,
      entrance_node_id,
      last_scheduled_row.species,
      last_scheduled_row.exhibit,
      last_scheduled_row.enclosure_name ) or entrance_node_id
   last_end_seconds = DateValues.time_value_in_seconds(
      last_scheduled_row.end_time ) or anchor_seconds

   return BulkScheduleStartState(
      start_node_id=start_node_id,
      schedule_anchor_seconds=max( anchor_seconds, last_end_seconds ) )
