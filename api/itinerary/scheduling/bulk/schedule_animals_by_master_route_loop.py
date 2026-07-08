from __future__ import annotations

from ..core.time_block import time_block_from_schedule_times
from ..core.time_block import TimeBlock
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_default_duration import fetch_enclosure_viewing_default_duration_seconds
from ...data_access.schedule_itinerary_item import update_itinerary_animal_schedule
from .loop_schedule_unit import LoopScheduleUnit
from .loop_unit_schedule_persist_error import LoopUnitSchedulePersistError
from .pack_loops_into_schedule_window import pack_loops_into_schedule_window
from .pack_loops_into_schedule_window import prepare_loop_schedule_units
from .pack_loops_into_schedule_window import PreparedLoopScheduleUnit
from .pack_loops_into_schedule_window import remove_matching_prepared_loop_unit
from ...routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from ....shared.calendar_dates import DateValues
from ....types import Connection
from ....types import ScheduleTimeKey
from ....walk_graph.domain.walk_graph import WalkGraph


LoopScheduleSlot = tuple[
   ItineraryAnimalRecord,
   ScheduleTimeKey,
   ScheduleTimeKey,
]


def schedule_animals_by_master_route_loop(
      conn: Connection,
      loop_units: list[ LoopScheduleUnit ],
      *,
      blockers: list[ TimeBlock ],
      schedule_windows: list[ ItineraryScheduleWindow ],
      schedule_cursor_seconds: int,
      walk_graph: WalkGraph,
      start_node_id: str ) -> tuple[ list[ ItineraryAnimalRecord ], int ]:
   prepared_units = prepare_loop_schedule_units( conn, loop_units )

   if prepared_units is None:
      return _animals_from_loop_units( loop_units ), schedule_cursor_seconds

   remaining_units = list( prepared_units )
   cursor_seconds = schedule_cursor_seconds
   window_index = 0
   current_node_id = start_node_id
   departure_side_cluster_id: str | None = None
   remaining_animals: list[ ItineraryAnimalRecord ] = []

   while remaining_units and window_index < len( schedule_windows ):
      window_index = _window_index_after_cursor(
         schedule_windows,
         window_index=window_index,
         cursor_seconds=cursor_seconds )

      if window_index >= len( schedule_windows ):
         break

      schedule_window = schedule_windows[ window_index ]

      if not _window_has_available_time(
            schedule_window,
            cursor_seconds=cursor_seconds ):
         cursor_seconds = schedule_window.end_seconds
         continue

      packed_units = pack_loops_into_schedule_window(
         walk_graph,
         schedule_window,
         prepared_units=remaining_units,
         cursor_seconds=cursor_seconds,
         current_node_id=current_node_id,
         departure_side_cluster_id=departure_side_cluster_id )

      if not packed_units:
         cursor_seconds = schedule_window.end_seconds
         continue

      cursor_seconds = _packed_units_start_seconds(
         schedule_window,
         packed_units=packed_units,
         cursor_seconds=cursor_seconds )

      for prepared_unit in packed_units:
         try:
            unscheduled_animals = _schedule_prepared_loop_unit(
               conn,
               prepared_unit,
               blockers=blockers,
               start_seconds=cursor_seconds )
         except LoopUnitSchedulePersistError as error:
            remaining_animals.extend( error.animals )
            remaining_animals.extend(
               _animals_from_prepared_units( remaining_units ) )
            return remaining_animals, cursor_seconds

         remaining_animals.extend( unscheduled_animals )

         if unscheduled_animals:
            continue

         remove_matching_prepared_loop_unit( remaining_units, prepared_unit )
         cursor_seconds += prepared_unit.duration_seconds

         if prepared_unit.unit.exit_walk_node_id is not None:
            current_node_id = prepared_unit.unit.exit_walk_node_id

         departure_side_cluster_id = prepared_unit.unit.side_cluster_id

   remaining_animals.extend(
      _animals_from_prepared_units( remaining_units ) )

   return remaining_animals, cursor_seconds


def _packed_units_start_seconds(
      schedule_window: ItineraryScheduleWindow,
      *,
      packed_units: list[ PreparedLoopScheduleUnit ],
      cursor_seconds: int ) -> int:
   window_start_seconds = max(
      cursor_seconds,
      schedule_window.start_seconds )

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
      start_seconds: int ) -> list[ ItineraryAnimalRecord ]:
   animals = list( prepared_unit.unit.animals )
   durations = _fetch_viewing_durations( conn, animals )

   if durations is None:
      return animals

   animal_slots, _ = _assign_contiguous_slots(
      animals,
      durations,
      start_seconds=start_seconds )

   if not animal_slots:
      return animals

   if not _save_loop_slots( conn, blockers, animal_slots ):
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


def _fetch_viewing_durations(
      conn: Connection,
      animals: list[ ItineraryAnimalRecord ] ) -> list[ int ] | None:
   durations: list[ int ] = []

   for animal_row in animals:
      duration_seconds = fetch_enclosure_viewing_default_duration_seconds(
         conn,
         animal_row.species,
         animal_row.exhibit,
         animal_row.enclosure_name )

      if duration_seconds is None:
         return None

      durations.append( duration_seconds )

   return durations


def _assign_contiguous_slots(
      animals: list[ ItineraryAnimalRecord ],
      durations: list[ int ],
      *,
      start_seconds: int ) -> tuple[ list[ LoopScheduleSlot ], int ]:
   slots: list[ LoopScheduleSlot ] = []
   slot_cursor_seconds = start_seconds

   for animal_row, duration_seconds in zip( animals, durations ):
      start_time = DateValues.schedule_time_key_from_seconds(
         slot_cursor_seconds )
      end_seconds = slot_cursor_seconds + duration_seconds
      end_time = DateValues.schedule_time_key_from_seconds( end_seconds )

      if start_time is None or end_time is None:
         return [], start_seconds

      slots.append( ( animal_row, start_time, end_time ) )
      slot_cursor_seconds = end_seconds

   return slots, slot_cursor_seconds


def _save_loop_slots(
      conn: Connection,
      blockers: list[ TimeBlock ],
      animal_slots: list[ LoopScheduleSlot ] ) -> bool:
   if not _persist_loop_group_slots( conn, tuple( animal_slots ) ):
      return False

   _append_slots_to_blockers( blockers, tuple( animal_slots ) )

   return True


def _append_slots_to_blockers(
      blockers: list[ TimeBlock ],
      slots: tuple[ LoopScheduleSlot, ... ] ) -> None:
   for _, start_time, end_time in slots:
      scheduled_block = time_block_from_schedule_times(
         start_time,
         end_time )

      if scheduled_block is not None:
         blockers.append( scheduled_block )


def _persist_loop_group_slots(
      conn: Connection,
      scheduled_slots: tuple[ LoopScheduleSlot, ... ] ) -> bool:
   cur = conn.cursor()

   try:
      for animal_row, start_time, end_time in scheduled_slots:
         if not update_itinerary_animal_schedule(
               cur,
               species=animal_row.species,
               exhibit=animal_row.exhibit,
               enclosure_name=animal_row.enclosure_name,
               start_time=start_time,
               end_time=end_time ):
            conn.rollback()
            return False

      conn.commit()
      return True

   finally:
      cur.close()
