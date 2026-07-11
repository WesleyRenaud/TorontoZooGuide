from __future__ import annotations

from ....animals.coordinators.animal_coordinator import AnimalCoordinator
from ....attractions.coordinators.attraction_coordinator import AttractionCoordinator
from .bulk_schedule_arrival_adjustment import adjust_arrival_after_bulk_schedule
from .bulk_schedule_departure import ensure_departure_after_bulk_schedule
from .bulk_schedule_loop_pins import attach_loop_pins_to_schedule_windows
from .bulk_schedule_loop_pins import separate_schedule_boundaries_and_loop_pins
from .bulk_schedule_start_state import BulkScheduleStartState
from .bulk_schedule_walk_order import representative_walk_node_id
from ..core.time_block import collect_time_blocks_from_itinerary
from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...domain.itinerary import build_current_itinerary
from ...domain.itinerary_adjustment import ItineraryAdjustment
from .group_animals_by_master_route_loop import group_animals_by_master_route_loop
from ....guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ..items.schedule_itinerary_helpers import build_itinerary_context
from ..items.schedule_itinerary_helpers import build_save_result
from ..items.schedule_itinerary_helpers import persist_itinerary_walk_route
from ..items.schedule_itinerary_helpers import prepare_schedule_window
from .loop_schedule_unit import build_loop_schedule_units
from ...results.itinerary_result_reason import ItineraryResultReason
from ...results.itinerary_save_result import ItinerarySaveResult
from ...routing.partition_itinerary_schedule_windows import partition_itinerary_schedule_windows
from ...routing.resolve_itinerary_stops import resolve_fixed_time_itinerary_stops
from .schedule_animals_by_master_route_loop import schedule_animals_by_master_route_loop
from ....shared.calendar_dates import DateValues
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ..unscheduling.clear_all_itinerary_schedules import clear_all_itinerary_schedules
from ....walk_graph.data_access.load_walk_graph import load_walk_graph
from ....walk_graph.domain.walk_graph import WalkGraph
from ...warnings.bulk_schedule_animals_warning import build_bulk_schedule_animals_not_enough_time_issue
from ....wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def has_itinerary_schedule_times(
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> bool:
   return bool(
      DateValues.normalize_schedule_time_key( start_time )
      and DateValues.normalize_schedule_time_key( end_time ) )


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
      animals_to_schedule: list[ ItineraryAnimalRecord ] ) -> ItinerarySaveResult:
   itinerary_context = build_itinerary_context(
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_coordinator=guardians_coordinator,
      wild_encounter_coordinator=wild_encounter_coordinator,
      visit_date_temp=visit_date_temp )

   if not animals_to_schedule:
      return build_save_result(
         conn,
         ItineraryErrorType.BULK_SCHEDULE_ANIMALS_ALREADY_SCHEDULED,
         **itinerary_context )

   saved_itinerary = fetch_saved_itinerary( conn )
   schedule_window = prepare_schedule_window(
      conn,
      saved_itinerary,
      ensure_arrival_at_zoo_open=True,
      **itinerary_context )

   if isinstance( schedule_window, ItinerarySaveResult ):
      return schedule_window

   saved_itinerary, window = schedule_window

   clear_all_itinerary_schedules( conn )

   saved_itinerary = fetch_saved_itinerary( conn )

   anchor_seconds, day_end_seconds = window
   itinerary = build_current_itinerary(
      saved_itinerary,
      **itinerary_context )
   blockers = collect_time_blocks_from_itinerary( itinerary )
   walk_graph = load_walk_graph()
   start_state = _bulk_schedule_start_state(
      walk_graph,
      saved_itinerary.animal_rows,
      anchor_seconds )

   sorted_loop_groups = group_animals_by_master_route_loop( animals_to_schedule )
   loop_units = build_loop_schedule_units( sorted_loop_groups )
   fixed_time_stops = resolve_fixed_time_itinerary_stops( itinerary )
   boundary_stops, loop_pins = separate_schedule_boundaries_and_loop_pins(
      conn,
      itinerary,
      fixed_time_stops )
   schedule_windows = attach_loop_pins_to_schedule_windows(
      partition_itinerary_schedule_windows(
         start_state.schedule_anchor_seconds,
         day_end_seconds,
         boundary_stops ),
      loop_pins )

   if not loop_units:
      persist_itinerary_walk_route( conn, **itinerary_context )

      return ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         itinerary=build_current_itinerary(
            fetch_saved_itinerary( conn ),
            **itinerary_context ) )

   remaining_animals, _ = schedule_animals_by_master_route_loop(
      conn,
      loop_units,
      blockers=blockers,
      schedule_windows=schedule_windows,
      schedule_cursor_seconds=start_state.schedule_anchor_seconds,
      walk_graph=walk_graph,
      start_node_id=start_state.start_node_id )

   adjustments: tuple[ ItineraryAdjustment, ... ] = ()
   arrival_adjustment = adjust_arrival_after_bulk_schedule(
      conn,
      schedule_anchor_seconds=start_state.schedule_anchor_seconds,
      previous_arrival_time=saved_itinerary.arrival_time )

   if arrival_adjustment is not None:
      adjustments = ( arrival_adjustment, )

   reasons: tuple[ ItineraryResultReason, ... ] = ()

   if remaining_animals:
      reasons = (
         build_bulk_schedule_animals_not_enough_time_issue(
            remaining_animals ),
      )
   else:
      ensure_departure_after_bulk_schedule(
         conn,
         build_current_itinerary(
            fetch_saved_itinerary( conn ),
            **itinerary_context ) )

   persist_itinerary_walk_route( conn, **itinerary_context )

   return ItinerarySaveResult(
      status=ItineraryErrorType.SUCCESS,
      reasons=reasons,
      adjustments=adjustments,
      itinerary=build_current_itinerary(
         fetch_saved_itinerary( conn ),
         **itinerary_context ) )


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
