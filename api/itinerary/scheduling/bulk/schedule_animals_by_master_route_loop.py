from __future__ import annotations

from dataclasses import dataclass
from dataclasses import replace

from ..core.time_block import TimeBlock
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from .loop_schedule_unit import LoopScheduleUnit
from .loop_unit_schedule_persist_error import LoopUnitSchedulePersistError
from .loop_unit_schedule_slots import assign_contiguous_slots
from .loop_unit_schedule_slots import fetch_viewing_durations
from .loop_unit_schedule_slots import LoopScheduleSlotSink
from .loop_unit_schedule_slots import save_loop_slots
from .pack_loops_into_schedule_window import pack_all_loops_before_deadline
from .pack_loops_into_schedule_window import pack_loops_into_schedule_window
from .pack_loops_into_schedule_window import prepare_loop_schedule_units
from .pack_loops_into_schedule_window import PreparedLoopScheduleUnit
from .pack_loops_into_schedule_window import remove_matching_prepared_loop_unit
from ...routing.loop_schedule_pin import LoopSchedulePin
from ...routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from .schedule_loop_unit_with_pins import pinned_loop_earliest_start_seconds
from .schedule_loop_unit_with_pins import schedule_prepared_loop_unit_with_pins
from ....types import Connection
from ....walk_graph.domain.walk_graph import WalkGraph


@dataclass
class _LoopScheduleWindowState:
   cursor_seconds: int
   current_node_id: str
   departure_side_cluster_id: str | None


def schedule_animals_by_master_route_loop(
      conn: Connection,
      loop_units: list[ LoopScheduleUnit ],
      *,
      blockers: list[ TimeBlock ],
      schedule_windows: list[ ItineraryScheduleWindow ],
      schedule_cursor_seconds: int,
      walk_graph: WalkGraph,
      start_node_id: str,
      slot_sink: LoopScheduleSlotSink | None = None ) -> tuple[ list[ ItineraryAnimalRecord ], int ]:
   prepared_units = prepare_loop_schedule_units( conn, loop_units )

   if prepared_units is None:
      return _animals_from_loop_units( loop_units ), schedule_cursor_seconds

   remaining_units = list( prepared_units )
   window_state = _LoopScheduleWindowState(
      cursor_seconds=schedule_cursor_seconds,
      current_node_id=start_node_id,
      departure_side_cluster_id=None )
   window_index = 0
   remaining_animals: list[ ItineraryAnimalRecord ] = []
   pinned_earliest_start_cache = _build_pinned_earliest_start_cache(
      conn,
      prepared_units,
      schedule_windows )

   while remaining_units and window_index < len( schedule_windows ):
      window_index = _window_index_after_cursor(
         schedule_windows,
         window_index=window_index,
         cursor_seconds=window_state.cursor_seconds )

      if window_index >= len( schedule_windows ):
         break

      schedule_window = schedule_windows[ window_index ]

      if not _window_has_available_time(
            schedule_window,
            cursor_seconds=window_state.cursor_seconds ):
         window_state.cursor_seconds = schedule_window.end_seconds
         continue

      cursor_before_window = window_state.cursor_seconds
      pinned_loop_ids = _pinned_loop_ids_in_window( schedule_window )
      should_abort = not _process_schedule_window(
         conn,
         remaining_units=remaining_units,
         schedule_window=schedule_window,
         pinned_loop_ids=pinned_loop_ids,
         pinned_earliest_start_cache=pinned_earliest_start_cache,
         blockers=blockers,
         walk_graph=walk_graph,
         window_state=window_state,
         remaining_animals=remaining_animals,
         slot_sink=slot_sink )

      if should_abort:
         return remaining_animals, window_state.cursor_seconds

      if window_state.cursor_seconds > cursor_before_window:
         continue

      wait_until_seconds = _earliest_pinned_loop_wait_seconds(
         remaining_units,
         pinned_loop_ids,
         pinned_earliest_start_cache=pinned_earliest_start_cache,
         cursor_seconds=window_state.cursor_seconds )

      if (
            wait_until_seconds is not None
            and wait_until_seconds > window_state.cursor_seconds
            and wait_until_seconds < schedule_window.end_seconds ):
         window_state.cursor_seconds = wait_until_seconds
         continue

      window_state.cursor_seconds = schedule_window.end_seconds

   remaining_animals.extend(
      _animals_from_prepared_units( remaining_units ) )

   return remaining_animals, window_state.cursor_seconds


def _process_schedule_window(
      conn: Connection,
      *,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      schedule_window: ItineraryScheduleWindow,
      pinned_loop_ids: set[ str ],
      pinned_earliest_start_cache: dict[ int, int | None ],
      blockers: list[ TimeBlock ],
      walk_graph: WalkGraph,
      window_state: _LoopScheduleWindowState,
      remaining_animals: list[ ItineraryAnimalRecord ],
      slot_sink: LoopScheduleSlotSink | None = None,
   ) -> bool:
   if pinned_loop_ids:
      packed_cursor_seconds, should_abort = _pack_non_pinned_loops_before_pinned_deadline(
         conn,
         remaining_units=remaining_units,
         schedule_window=schedule_window,
         pinned_loop_ids=pinned_loop_ids,
         pinned_earliest_start_cache=pinned_earliest_start_cache,
         blockers=blockers,
         walk_graph=walk_graph,
         window_state=window_state,
         remaining_animals=remaining_animals,
         slot_sink=slot_sink )

      if should_abort:
         return False

      window_state.cursor_seconds = packed_cursor_seconds

   if pinned_loop_ids:
      window_state.cursor_seconds = _drain_ready_pinned_loop_units(
         conn,
         remaining_units,
         schedule_window,
         pinned_earliest_start_cache=pinned_earliest_start_cache,
         blockers=blockers,
         cursor_seconds=window_state.cursor_seconds,
         slot_sink=slot_sink )

   packing_window = _non_pinned_packing_window(
      schedule_window,
      remaining_units=remaining_units,
      pinned_loop_ids=pinned_loop_ids,
      pinned_earliest_start_cache=pinned_earliest_start_cache,
      cursor_seconds=window_state.cursor_seconds )
   packed_units = pack_loops_into_schedule_window(
      walk_graph,
      packing_window,
      prepared_units=_units_excluding_pinned_loops(
         remaining_units,
         pinned_loop_ids ),
      cursor_seconds=window_state.cursor_seconds,
      current_node_id=window_state.current_node_id,
      departure_side_cluster_id=window_state.departure_side_cluster_id )

   if packed_units:
      window_state.cursor_seconds = _schedule_start_seconds_for_packed_units(
         packing_window,
         packed_units=packed_units,
         cursor_seconds=window_state.cursor_seconds )

      for prepared_unit in packed_units:
         try:
            unscheduled_animals = _schedule_prepared_loop_unit(
               conn,
               prepared_unit,
               blockers=blockers,
               start_seconds=window_state.cursor_seconds,
               slot_sink=slot_sink )
         except LoopUnitSchedulePersistError as error:
            remaining_animals.extend( error.animals )
            remaining_animals.extend(
               _animals_from_prepared_units( remaining_units ) )
            return False

         remaining_animals.extend( unscheduled_animals )

         if unscheduled_animals:
            continue

         remove_matching_prepared_loop_unit( remaining_units, prepared_unit )
         window_state.cursor_seconds += prepared_unit.duration_seconds

         if prepared_unit.unit.exit_walk_node_id is not None:
            window_state.current_node_id = prepared_unit.unit.exit_walk_node_id

         window_state.departure_side_cluster_id = prepared_unit.unit.side_cluster_id

         if pinned_loop_ids:
            window_state.cursor_seconds = _drain_ready_pinned_loop_units(
               conn,
               remaining_units,
               schedule_window,
               pinned_earliest_start_cache=pinned_earliest_start_cache,
               blockers=blockers,
               cursor_seconds=window_state.cursor_seconds,
               slot_sink=slot_sink )

   if pinned_loop_ids:
      window_state.cursor_seconds = _drain_ready_pinned_loop_units(
         conn,
         remaining_units,
         schedule_window,
         pinned_earliest_start_cache=pinned_earliest_start_cache,
         blockers=blockers,
         cursor_seconds=window_state.cursor_seconds,
         slot_sink=slot_sink )

   return True


def _non_pinned_packing_window(
      schedule_window: ItineraryScheduleWindow,
      *,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      pinned_loop_ids: set[ str ],
      pinned_earliest_start_cache: dict[ int, int | None ],
      cursor_seconds: int,
   ) -> ItineraryScheduleWindow:
   """Cap packing so other loops cannot steal a pinned loop's before-pin window."""
   if not pinned_loop_ids:
      return schedule_window

   reserved_start_seconds = _earliest_pinned_loop_wait_seconds(
      remaining_units,
      pinned_loop_ids,
      pinned_earliest_start_cache=pinned_earliest_start_cache,
      cursor_seconds=cursor_seconds )

   if (
         reserved_start_seconds is None
         or reserved_start_seconds >= schedule_window.end_seconds ):
      return schedule_window

   return replace(
      schedule_window,
      end_seconds=reserved_start_seconds )


def _pack_non_pinned_loops_before_pinned_deadline(
      conn: Connection,
      *,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      schedule_window: ItineraryScheduleWindow,
      pinned_loop_ids: set[ str ],
      pinned_earliest_start_cache: dict[ int, int | None ],
      blockers: list[ TimeBlock ],
      walk_graph: WalkGraph,
      window_state: _LoopScheduleWindowState,
      remaining_animals: list[ ItineraryAnimalRecord ],
      slot_sink: LoopScheduleSlotSink | None = None,
   ) -> tuple[ int, bool ]:
   non_pinned_units = _units_excluding_pinned_loops(
      remaining_units,
      pinned_loop_ids )

   if not non_pinned_units:
      return window_state.cursor_seconds, False

   pinned_deadline_seconds = _earliest_pinned_loop_wait_seconds(
      remaining_units,
      pinned_loop_ids,
      pinned_earliest_start_cache=pinned_earliest_start_cache,
      cursor_seconds=window_state.cursor_seconds )

   if (
         pinned_deadline_seconds is None
         or window_state.cursor_seconds >= pinned_deadline_seconds ):
      return window_state.cursor_seconds, False

   window_start_seconds = _packed_units_start_seconds(
      schedule_window,
      cursor_seconds=window_state.cursor_seconds )
   packed_units = pack_all_loops_before_deadline(
      walk_graph,
      prepared_units=non_pinned_units,
      window_start_seconds=window_start_seconds,
      deadline_seconds=pinned_deadline_seconds,
      current_node_id=window_state.current_node_id,
      departure_side_cluster_id=window_state.departure_side_cluster_id )

   if packed_units is None:
      return window_state.cursor_seconds, False

   total_duration_seconds = sum(
      prepared_unit.duration_seconds
      for prepared_unit in packed_units )
   schedule_start_seconds = pinned_deadline_seconds - total_duration_seconds

   for prepared_unit in packed_units:
      try:
         unscheduled_animals = _schedule_prepared_loop_unit(
            conn,
            prepared_unit,
            blockers=blockers,
            start_seconds=schedule_start_seconds,
            slot_sink=slot_sink )
      except LoopUnitSchedulePersistError as error:
         remaining_animals.extend( error.animals )
         remaining_animals.extend(
            _animals_from_prepared_units( remaining_units ) )
         return window_state.cursor_seconds, True

      if unscheduled_animals:
         remaining_animals.extend( unscheduled_animals )
         return window_state.cursor_seconds, False

      remove_matching_prepared_loop_unit( remaining_units, prepared_unit )
      schedule_start_seconds += prepared_unit.duration_seconds

      if prepared_unit.unit.exit_walk_node_id is not None:
         window_state.current_node_id = prepared_unit.unit.exit_walk_node_id

      window_state.departure_side_cluster_id = prepared_unit.unit.side_cluster_id

   return pinned_deadline_seconds, False


def _build_pinned_earliest_start_cache(
      conn: Connection,
      prepared_units: list[ PreparedLoopScheduleUnit ],
      schedule_windows: list[ ItineraryScheduleWindow ],
   ) -> dict[ int, int | None ]:
   pinned_loop_ids = {
      loop_pin.loop_id
      for schedule_window in schedule_windows
      for loop_pin in schedule_window.loop_pins
   }

   if not pinned_loop_ids:
      return {}

   loop_pins = [
      loop_pin
      for schedule_window in schedule_windows
      for loop_pin in schedule_window.loop_pins
   ]
   cache: dict[ int, int | None ] = {}

   for prepared_unit in prepared_units:
      loop_id = prepared_unit.unit.loop_id

      if loop_id is None or loop_id not in pinned_loop_ids:
         continue

      cache[ id( prepared_unit ) ] = pinned_loop_earliest_start_seconds(
         conn,
         prepared_unit,
         loop_pins )

   return cache


def _drain_ready_pinned_loop_units(
      conn: Connection,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      schedule_window: ItineraryScheduleWindow,
      *,
      pinned_earliest_start_cache: dict[ int, int | None ],
      blockers: list[ TimeBlock ],
      cursor_seconds: int,
      slot_sink: LoopScheduleSlotSink | None = None,
   ) -> int:
   pinned_loop_ids = _pinned_loop_ids_in_window( schedule_window )
   schedule_cursor_seconds = cursor_seconds

   while True:
      made_progress = False

      for prepared_unit in _ready_pinned_loop_units(
            remaining_units,
            pinned_loop_ids,
            pinned_earliest_start_cache=pinned_earliest_start_cache,
            cursor_seconds=schedule_cursor_seconds ):
         unscheduled_animals, new_cursor_seconds = schedule_prepared_loop_unit_with_pins(
            conn,
            prepared_unit,
            schedule_window.loop_pins,
            blockers=blockers,
            window_start_seconds=schedule_window.start_seconds,
            window_end_seconds=schedule_window.end_seconds,
            cursor_seconds=schedule_cursor_seconds,
            slot_sink=slot_sink )

         if not unscheduled_animals:
            remove_matching_prepared_loop_unit( remaining_units, prepared_unit )
            schedule_cursor_seconds = new_cursor_seconds
            made_progress = True
            continue

         if _keep_partial_pinned_loop_progress(
               conn,
               remaining_units,
               prepared_unit,
               unscheduled_animals=unscheduled_animals,
               pinned_earliest_start_cache=pinned_earliest_start_cache,
               loop_pins=schedule_window.loop_pins ):
            schedule_cursor_seconds = max(
               schedule_cursor_seconds,
               new_cursor_seconds )
            made_progress = True
            break

      if not made_progress:
         break

   return schedule_cursor_seconds


def _keep_partial_pinned_loop_progress(
      conn: Connection,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      prepared_unit: PreparedLoopScheduleUnit,
      *,
      unscheduled_animals: list[ ItineraryAnimalRecord ],
      pinned_earliest_start_cache: dict[ int, int | None ],
      loop_pins: list[ LoopSchedulePin ],
   ) -> bool:
   original_animals = prepared_unit.unit.animals

   if len( unscheduled_animals ) >= len( original_animals ):
      return False

   durations = fetch_viewing_durations( conn, unscheduled_animals )

   if durations is None:
      return False

   replacement = PreparedLoopScheduleUnit(
      unit=replace(
         prepared_unit.unit,
         animals=tuple( unscheduled_animals ) ),
      duration_seconds=sum( durations ) )

   for index, candidate in enumerate( remaining_units ):
      if candidate is not prepared_unit:
         continue

      remaining_units[ index ] = replacement
      pinned_earliest_start_cache.pop( id( prepared_unit ), None )
      pinned_earliest_start_cache[ id( replacement ) ] = (
         pinned_loop_earliest_start_seconds(
            conn,
            replacement,
            loop_pins ) )
      return True

   return False


def _pinned_loop_ids_in_window(
      schedule_window: ItineraryScheduleWindow ) -> set[ str ]:
   return {
      loop_pin.loop_id
      for loop_pin in schedule_window.loop_pins
   }


def _units_excluding_pinned_loops(
      prepared_units: list[ PreparedLoopScheduleUnit ],
      pinned_loop_ids: set[ str ],
   ) -> list[ PreparedLoopScheduleUnit ]:
   return [
      prepared_unit
      for prepared_unit in prepared_units
      if prepared_unit.unit.loop_id not in pinned_loop_ids
   ]


def _ready_pinned_loop_units(
      prepared_units: list[ PreparedLoopScheduleUnit ],
      pinned_loop_ids: set[ str ],
      *,
      pinned_earliest_start_cache: dict[ int, int | None ],
      cursor_seconds: int,
   ) -> list[ PreparedLoopScheduleUnit ]:
   return [
      prepared_unit
      for prepared_unit in prepared_units
      if prepared_unit.unit.loop_id in pinned_loop_ids
      and _pinned_loop_is_ready(
         prepared_unit,
         pinned_earliest_start_cache=pinned_earliest_start_cache,
         cursor_seconds=cursor_seconds )
   ]


def _pinned_loop_is_ready(
      prepared_unit: PreparedLoopScheduleUnit,
      *,
      pinned_earliest_start_cache: dict[ int, int | None ],
      cursor_seconds: int,
   ) -> bool:
   earliest_start_seconds = pinned_earliest_start_cache.get(
      id( prepared_unit ) )

   if earliest_start_seconds is None:
      return False

   return cursor_seconds >= earliest_start_seconds


def _earliest_pinned_loop_wait_seconds(
      remaining_units: list[ PreparedLoopScheduleUnit ],
      pinned_loop_ids: set[ str ],
      *,
      pinned_earliest_start_cache: dict[ int, int | None ],
      cursor_seconds: int,
   ) -> int | None:
   wait_until_seconds: int | None = None

   for prepared_unit in remaining_units:
      if prepared_unit.unit.loop_id not in pinned_loop_ids:
         continue

      earliest_start_seconds = pinned_earliest_start_cache.get(
         id( prepared_unit ) )

      if earliest_start_seconds is None:
         continue

      if earliest_start_seconds <= cursor_seconds:
         continue

      wait_until_seconds = (
         earliest_start_seconds
         if wait_until_seconds is None
         else min( wait_until_seconds, earliest_start_seconds ) )

   return wait_until_seconds


def _packed_units_start_seconds(
      schedule_window: ItineraryScheduleWindow,
      *,
      cursor_seconds: int ) -> int:
   return max(
      cursor_seconds,
      schedule_window.start_seconds )


def _schedule_start_seconds_for_packed_units(
      schedule_window: ItineraryScheduleWindow,
      *,
      packed_units: list[ PreparedLoopScheduleUnit ],
      cursor_seconds: int ) -> int:
   window_start_seconds = _packed_units_start_seconds(
      schedule_window,
      cursor_seconds=cursor_seconds )

   if schedule_window.anchor_stop is None:
      return window_start_seconds

   total_duration_seconds = sum(
      prepared_unit.duration_seconds
      for prepared_unit in packed_units )

   return max(
      window_start_seconds,
      schedule_window.end_seconds - total_duration_seconds )


def _schedule_prepared_loop_unit(
      conn: Connection,
      prepared_unit: PreparedLoopScheduleUnit,
      *,
      blockers: list[ TimeBlock ],
      start_seconds: int,
      slot_sink: LoopScheduleSlotSink | None = None ) -> list[ ItineraryAnimalRecord ]:
   animals = list( prepared_unit.unit.animals )
   durations = fetch_viewing_durations( conn, animals )

   if durations is None:
      return animals

   animal_slots, _ = assign_contiguous_slots(
      animals,
      durations,
      start_seconds=start_seconds )

   if not animal_slots:
      return animals

   if not save_loop_slots(
         conn,
         blockers,
         animal_slots,
         slot_sink=slot_sink ):
      raise LoopUnitSchedulePersistError( animals )

   return []


def _window_has_available_time(
      schedule_window: ItineraryScheduleWindow,
      *,
      cursor_seconds: int ) -> bool:
   return max(
      cursor_seconds,
      schedule_window.start_seconds ) < schedule_window.end_seconds


def _window_index_after_cursor(
      schedule_windows: list[ ItineraryScheduleWindow ],
      *,
      window_index: int,
      cursor_seconds: int ) -> int:
   while _cursor_has_passed_schedule_window(
         schedule_windows,
         window_index=window_index,
         cursor_seconds=cursor_seconds ):
      window_index += 1

   return window_index


def _cursor_has_passed_schedule_window(
      schedule_windows: list[ ItineraryScheduleWindow ],
      *,
      window_index: int,
      cursor_seconds: int ) -> bool:
   if window_index >= len( schedule_windows ):
      return False

   return cursor_seconds >= schedule_windows[ window_index ].end_seconds


def _animals_from_loop_units(
      loop_units: list[ LoopScheduleUnit ] ) -> list[ ItineraryAnimalRecord ]:
   return [
      animal_row
      for loop_unit in loop_units
      for animal_row in loop_unit.animals
   ]


def _animals_from_prepared_units(
      prepared_units: list[ PreparedLoopScheduleUnit ] ) -> list[
         ItineraryAnimalRecord,
   ]:
   return [
      animal_row
      for prepared_unit in prepared_units
      for animal_row in prepared_unit.unit.animals
   ]
