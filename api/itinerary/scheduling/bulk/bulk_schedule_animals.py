from __future__ import annotations

from ....animals.coordinators.animal_coordinator import AnimalCoordinator
from ....attractions.coordinators.attraction_coordinator import AttractionCoordinator
from .bulk_schedule_start_state import BulkScheduleStartState
from .bulk_schedule_walk_order import representative_walk_node_id
from .bulk_schedule_walk_order import sort_animals_for_bulk_schedule
from ..core.resolve_schedule_slot import resolve_schedule_slot
from ..core.time_block import collect_time_blocks_from_itinerary
from ..core.time_block import time_block_from_schedule_times
from ..core.time_block import TimeBlock
from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_default_duration import fetch_enclosure_default_duration_seconds
from ...data_access.schedule_itinerary_item import update_itinerary_animal_schedule
from ...domain.itinerary import build_current_itinerary
from ....guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ..items.schedule_itinerary_helpers import build_itinerary_context
from ..items.schedule_itinerary_helpers import resolve_schedule_window
from ...results.itinerary_result_reason import ItineraryResultReason
from ...results.itinerary_save_result import ItinerarySaveResult
from ...routing.persist_itinerary_walk_route import rebuild_and_persist_itinerary_walk_route
from ....shared.calendar_dates import DateValues
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ....types import Cursor
from ....types import ScheduleTimeKey
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
      visit_date_temp: float | None = None ) -> ItinerarySaveResult:
   itinerary_context = build_itinerary_context(
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_coordinator=guardians_coordinator,
      wild_encounter_coordinator=wild_encounter_coordinator,
      visit_date_temp=visit_date_temp )

   saved_itinerary = fetch_saved_itinerary( conn )
   window = resolve_schedule_window(
      conn,
      saved_itinerary,
      **itinerary_context )

   if isinstance( window, ItinerarySaveResult ):
      return window

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

   unscheduled_animals = sort_animals_for_bulk_schedule(
      walk_graph,
      [
         animal_row
         for animal_row in saved_itinerary.animal_rows
         if is_itinerary_animal_unscheduled( animal_row )
      ],
      start_node_id=start_state.start_node_id )

   if not unscheduled_animals:
      status = (
         ItineraryErrorType.BULK_SCHEDULE_ANIMALS_ALREADY_SCHEDULED
         if saved_itinerary.animal_rows
         else ItineraryErrorType.SUCCESS
      )

      _persist_itinerary_walk_route( conn, **itinerary_context )

      return ItinerarySaveResult(
         status=status,
         itinerary=build_current_itinerary(
            fetch_saved_itinerary( conn ),
            **itinerary_context ) )

   remaining_animals = _schedule_animals_in_order(
      conn,
      unscheduled_animals,
      blockers=blockers,
      anchor_seconds=start_state.schedule_anchor_seconds,
      day_end_seconds=day_end_seconds )

   reasons: tuple[ ItineraryResultReason, ... ] = ()

   if remaining_animals:
      reasons = (
         build_bulk_schedule_animals_not_enough_time_issue(
            remaining_animals ),
      )

   _persist_itinerary_walk_route( conn, **itinerary_context )

   return ItinerarySaveResult(
      status=ItineraryErrorType.SUCCESS,
      reasons=reasons,
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
      last_scheduled_row.exhibit ) or entrance_node_id
   last_end_seconds = DateValues.time_value_in_seconds(
      last_scheduled_row.end_time ) or anchor_seconds

   return BulkScheduleStartState(
      start_node_id=start_node_id,
      schedule_anchor_seconds=max( anchor_seconds, last_end_seconds ) )


def _schedule_animals_in_order(
      conn: Connection,
      animals: list[ ItineraryAnimalRecord ],
      *,
      blockers: list[ TimeBlock ],
      anchor_seconds: int,
      day_end_seconds: int ) -> list[ ItineraryAnimalRecord ]:
   cur = conn.cursor()
   scheduled_count = 0

   try:
      for index, animal_row in enumerate( animals ):
         duration_seconds = fetch_enclosure_default_duration_seconds(
            conn,
            animal_row.species,
            animal_row.exhibit )

         if duration_seconds is None:
            _commit_scheduled_animals( conn, scheduled_count )
            return animals[ index: ]

         slot = resolve_schedule_slot(
            blockers,
            anchor_seconds,
            duration_seconds,
            day_end_seconds,
            start_time=None )

         if slot is None:
            _commit_scheduled_animals( conn, scheduled_count )
            return animals[ index: ]

         start_time, end_time = slot

         if not _persist_animal_schedule(
               cur,
               animal_row=animal_row,
               start_time=start_time,
               end_time=end_time ):
            _commit_scheduled_animals( conn, scheduled_count )
            return animals[ index: ]

         scheduled_count += 1

         scheduled_block = time_block_from_schedule_times(
            start_time,
            end_time )

         if scheduled_block is not None:
            blockers.append( scheduled_block )

      conn.commit()
      return []

   finally:
      cur.close()


def _commit_scheduled_animals(
      conn: Connection,
      scheduled_count: int ) -> None:
   if scheduled_count > 0:
      conn.commit()


def _persist_animal_schedule(
      cur: Cursor,
      *,
      animal_row: ItineraryAnimalRecord,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> bool:
   return update_itinerary_animal_schedule(
      cur,
      species=animal_row.species,
      exhibit=animal_row.exhibit,
      start_time=start_time,
      end_time=end_time )


def _persist_itinerary_walk_route(
      conn: Connection,
      *,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      visit_date_temp: float | None = None ) -> None:
   rebuild_and_persist_itinerary_walk_route(
      conn,
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_coordinator=guardians_coordinator,
      wild_encounter_coordinator=wild_encounter_coordinator,
      visit_date_temp=visit_date_temp )
