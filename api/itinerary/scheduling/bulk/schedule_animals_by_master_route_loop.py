from __future__ import annotations

from dataclasses import dataclass
from dataclasses import replace

from .attraction_hours_soft_pin_resolver import AttractionHoursSoftPinResolver
from ..core.time_block import TimeBlock
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from .loop_schedule_stop import LoopScheduleStop
from .loop_schedule_stop_extractor import LoopScheduleStopExtractor
from .loop_schedule_unit import LoopScheduleUnit
from .loop_unit_schedule_persist_error import LoopUnitSchedulePersistError
from .loop_unit_schedule_slots import assign_contiguous_slots_respecting_attraction_hours
from .loop_unit_schedule_slots import LoopScheduleSlotSink
from .loop_unit_schedule_slots import prepare_loop_schedule_stops
from .loop_unit_schedule_slots import save_loop_slots
from .loop_unit_schedule_slots import total_occupied_seconds
from .loop_unit_travel_time import approach_travel_seconds_to_unit
from .loop_unit_travel_time import packed_units_occupied_seconds
from .pack_loops_into_schedule_window import pack_all_loops_before_deadline
from .pack_loops_into_schedule_window import pack_loops_into_schedule_window
from .pack_loops_into_schedule_window import prepare_loop_schedule_units
from .pack_loops_into_schedule_window import PreparedLoopScheduleUnit
from .pack_loops_into_schedule_window import remove_matching_prepared_loop_unit
from ...routing.attraction_hours_soft_pin import AttractionHoursSoftPin
from ...routing.loop_schedule_pin import LoopSchedulePin
from ...routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from .schedule_loop_unit_with_attraction_hours import attraction_hours_loop_earliest_start_seconds
from .schedule_loop_unit_with_attraction_hours import schedule_prepared_loop_unit_with_attraction_hours
from .schedule_loop_unit_with_pins import pinned_loop_earliest_start_seconds
from .schedule_loop_unit_with_pins import schedule_prepared_loop_unit_with_pins
from ....shared.calendar_dates import DateValues
from ....shared.operating_hours import OperatingHours
from ....types import Connection
from ....walk_graph.data_access.load_walk_graph import load_walk_graph
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
      slot_sink: LoopScheduleSlotSink | None = None ) -> tuple[ list[ LoopScheduleStop ], int ]:
   prepared_units = prepare_loop_schedule_units(
      conn,
      loop_units,
      walk_graph=walk_graph )

   if prepared_units is None:
      return _animals_from_loop_units( loop_units ), schedule_cursor_seconds

   remaining_units = list( prepared_units )
   window_state = _LoopScheduleWindowState(
      cursor_seconds=schedule_cursor_seconds,
      current_node_id=start_node_id,
      departure_side_cluster_id=None )
   window_index = 0
   remaining_animals: list[ LoopScheduleStop ] = []
   pinned_earliest_start_cache = _build_constrained_earliest_start_cache(
      conn,
      prepared_units,
      schedule_windows )
   held_pinned_loop_ids = {
      loop_pin.loop_id
      for schedule_window in schedule_windows
      for loop_pin in schedule_window.loop_pins
   }
   held_soft_pin_loop_ids = {
      soft_pin.loop_id
      for schedule_window in schedule_windows
      for soft_pin in schedule_window.attraction_hours_soft_pins
   }
   held_constrained_loop_ids = held_pinned_loop_ids | held_soft_pin_loop_ids
   hours_by_attraction_name = AttractionHoursSoftPinResolver.hours_by_name(
      [
         soft_pin
         for schedule_window in schedule_windows
         for soft_pin in schedule_window.attraction_hours_soft_pins
      ] )

   while remaining_units and window_index < len( schedule_windows ):
      window_index = _window_index_after_cursor(
         schedule_windows,
         window_index=window_index,
         cursor_seconds=window_state.cursor_seconds )

      if window_index >= len( schedule_windows ):
         break

      schedule_window = schedule_windows[ window_index ]

      if (
            schedule_window.start_walk_node_id is not None
            and window_state.cursor_seconds <= schedule_window.start_seconds ):
         window_state.current_node_id = schedule_window.start_walk_node_id

      if not _window_has_available_time(
            schedule_window,
            cursor_seconds=window_state.cursor_seconds ):
         window_state.cursor_seconds = schedule_window.end_seconds
         continue

      cursor_before_window = window_state.cursor_seconds
      pinned_loop_ids = _pinned_loop_ids_in_window( schedule_window )
      remaining_soft_pins = _remaining_soft_pins_in_window(
         schedule_window,
         remaining_units )
      active_soft_pin_loop_ids = _active_soft_pin_loop_ids( remaining_soft_pins )
      # Wait for hard pins or the active soft pin's open (wait-filler). Also wake
      # for inactive soft pins that open earlier so Zoomobile can fill the wait
      # before Face Painting instead of leaving a dead morning gap.
      wait_constrained_loop_ids = (
         pinned_loop_ids
         | active_soft_pin_loop_ids
         | _inactive_soft_pin_loop_ids_opening_before_active(
            schedule_window,
            remaining_units,
            active_soft_pin_loop_ids=active_soft_pin_loop_ids,
            cursor_seconds=window_state.cursor_seconds ) )
      should_abort = not _process_schedule_window(
         conn,
         remaining_units=remaining_units,
         schedule_window=schedule_window,
         later_schedule_windows=schedule_windows[ window_index + 1 : ],
         pinned_loop_ids=pinned_loop_ids,
         active_soft_pin_loop_ids=active_soft_pin_loop_ids,
         held_constrained_loop_ids=held_constrained_loop_ids,
         pinned_earliest_start_cache=pinned_earliest_start_cache,
         hours_by_attraction_name=hours_by_attraction_name,
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
         wait_constrained_loop_ids,
         pinned_earliest_start_cache=pinned_earliest_start_cache,
         cursor_seconds=window_state.cursor_seconds )

      if (
            wait_until_seconds is not None
            and wait_until_seconds > window_state.cursor_seconds
            and wait_until_seconds < schedule_window.end_seconds ):
         window_state.cursor_seconds = wait_until_seconds
         continue

      window_state.cursor_seconds = schedule_window.end_seconds

   return (
      _animals_from_prepared_units( remaining_units ),
      window_state.cursor_seconds )


def _process_schedule_window(
      conn: Connection,
      *,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      schedule_window: ItineraryScheduleWindow,
      later_schedule_windows: list[ ItineraryScheduleWindow ],
      pinned_loop_ids: set[ str ],
      active_soft_pin_loop_ids: set[ str ],
      held_constrained_loop_ids: set[ str ],
      pinned_earliest_start_cache: dict[ int, int | None ],
      hours_by_attraction_name: dict[ str, OperatingHours ],
      blockers: list[ TimeBlock ],
      walk_graph: WalkGraph,
      window_state: _LoopScheduleWindowState,
      remaining_animals: list[ LoopScheduleStop ],
      slot_sink: LoopScheduleSlotSink | None = None,
   ) -> bool:
   hard_pinned_loop_ids = set( pinned_loop_ids )
   active_open_seconds = _earliest_active_soft_pin_open_seconds(
      schedule_window,
      active_soft_pin_loop_ids )
   wait_filler_pending = (
         bool( active_soft_pin_loop_ids )
         and active_open_seconds is not None
         and window_state.cursor_seconds < active_open_seconds )

   # Hard pins only for right-align-before-deadline. Soft pins use wait-filler /
   # late-place paths instead of forcing a full pre-open pack of every loop.
   # While waiting on an active soft pin, skip this — packing Greenhouse/Americas
   # flush against the hard pin steals the Carousel→Zoomobile→Face Painting slots.
   if hard_pinned_loop_ids and not wait_filler_pending:
      packed_cursor_seconds, should_abort = _pack_non_pinned_loops_before_pinned_deadline(
         conn,
         remaining_units=remaining_units,
         schedule_window=schedule_window,
         pinned_loop_ids=hard_pinned_loop_ids,
         exclude_loop_ids=held_constrained_loop_ids,
         pinned_earliest_start_cache=pinned_earliest_start_cache,
         hours_by_attraction_name=hours_by_attraction_name,
         blockers=blockers,
         walk_graph=walk_graph,
         window_state=window_state,
         remaining_animals=remaining_animals,
         slot_sink=slot_sink )

      if should_abort:
         return False

      window_state.cursor_seconds = packed_cursor_seconds

   if hard_pinned_loop_ids and not wait_filler_pending:
      window_state.cursor_seconds = _drain_ready_pinned_loop_units(
         conn,
         remaining_units,
         schedule_window,
         pinned_earliest_start_cache=pinned_earliest_start_cache,
         blockers=blockers,
         cursor_seconds=window_state.cursor_seconds,
         slot_sink=slot_sink )

   if _should_defer_free_packing_until_after_anchor(
         schedule_window,
         later_schedule_windows=later_schedule_windows,
         remaining_units=remaining_units,
         held_pinned_loop_ids=held_constrained_loop_ids,
         pinned_earliest_start_cache=pinned_earliest_start_cache,
         cursor_seconds=window_state.cursor_seconds ):
      return True

   # Already-open soft pins ahead of a hard pin should late-place against that
   # pin (Face Painting beside Giraffe), not sit at first open with a dead gap.
   hard_pin_deadline_seconds = _earliest_hard_pin_deadline_seconds(
      remaining_units,
      hard_pinned_loop_ids,
      pinned_earliest_start_cache=pinned_earliest_start_cache )

   if (
         active_soft_pin_loop_ids
         and not wait_filler_pending
         and active_open_seconds is not None
         and window_state.cursor_seconds >= active_open_seconds
         and hard_pin_deadline_seconds is not None ):
      window_state.cursor_seconds, window_state.current_node_id = (
         _drain_ready_soft_pin_loop_units(
            conn,
            remaining_units,
            schedule_window,
            soft_only_loop_ids=active_soft_pin_loop_ids - hard_pinned_loop_ids,
            hard_pinned_loop_ids=hard_pinned_loop_ids,
            pinned_earliest_start_cache=pinned_earliest_start_cache,
            blockers=blockers,
            cursor_seconds=window_state.cursor_seconds,
            current_node_id=window_state.current_node_id,
            walk_graph=walk_graph,
            late_place=True,
            window_end_seconds=hard_pin_deadline_seconds,
            slot_sink=slot_sink ) )

   packing_hold_loop_ids = set( held_constrained_loop_ids )
   pack_open_soft_pins_with_free_loops = _should_pack_open_soft_pins_with_free_loops(
      remaining_units=remaining_units,
      active_soft_pin_loop_ids=active_soft_pin_loop_ids,
      held_constrained_loop_ids=held_constrained_loop_ids,
      wait_filler_pending=wait_filler_pending,
      hard_pin_deadline_seconds=hard_pin_deadline_seconds,
      active_open_seconds=active_open_seconds,
      cursor_seconds=window_state.cursor_seconds )

   if pack_open_soft_pins_with_free_loops:
      packing_hold_loop_ids -= active_soft_pin_loop_ids

   # Incomplete hard-pinned loops (rainforest leftovers after a talk weave) must
   # finish before later same-cluster loops — otherwise Carousel/Savanna insert
   # mid-corridor and split the pavilion.
   remaining_hard_pin_loop_ids = {
      prepared_unit.unit.loop_id
      for prepared_unit in remaining_units
      if prepared_unit.unit.loop_id in hard_pinned_loop_ids
   }

   if remaining_hard_pin_loop_ids:
      packing_hold_loop_ids |= _later_same_cluster_loop_ids(
         remaining_units,
         remaining_hard_pin_loop_ids )
   elif schedule_window.opens_after_fixed_time_stop:
      packing_hold_loop_ids |= _side_cluster_successor_loop_ids(
         remaining_units,
         held_constrained_loop_ids )

   if active_soft_pin_loop_ids and not pack_open_soft_pins_with_free_loops:
      # Wait-filler / hard-pin: later same-cluster loops (Greenhouse after
      # Walk-Thru) belong after the active soft pin on that corridor.
      packing_hold_loop_ids |= _later_same_cluster_loop_ids(
         remaining_units,
         active_soft_pin_loop_ids )

   # During wait-fill, keep inactive soft pins (Carousel, Zoomobile) out of the
   # free-pack wave. Releasing them let nearer free animals (Americas) skip
   # Carousel; they late-place against the cascade deadline after free packs.

   # Hard pins only. Inactive soft-pin opens must not truncate this window to
   # Carousel@9:30 / Zoomobile@10:00 — that left-packs Greenhouse into a 15-minute
   # pocket and late-packs Carousel against Zoomobile open with dead gaps. Soft-pin
   # slots are reserved below via wait_pack_end / active soft-pin tail reserve.
   packing_window = _non_pinned_packing_window(
      schedule_window,
      remaining_units=remaining_units,
      pinned_loop_ids=hard_pinned_loop_ids,
      pinned_earliest_start_cache=pinned_earliest_start_cache,
      cursor_seconds=window_state.cursor_seconds )

   wait_pack_planned_active_start_seconds: int | None = None

   if wait_filler_pending and active_open_seconds is not None:
      # Fill the wait before soft-pin open. Cascade-reserve the active soft pin
      # and inactive soft pins that open before it (Carousel, Zoomobile) so free
      # loops like Greenhouse right-align against the contiguous chain.
      wait_pack_end_seconds, wait_pack_planned_active_start_seconds = (
         _wait_filler_pack_end_seconds(
            schedule_window,
            remaining_units=remaining_units,
            active_soft_pin_loop_ids=active_soft_pin_loop_ids,
            hard_pinned_loop_ids=hard_pinned_loop_ids,
            active_open_seconds=active_open_seconds,
            hard_pin_deadline_seconds=hard_pin_deadline_seconds,
            cursor_seconds=window_state.cursor_seconds ) )

      packing_window = replace(
         packing_window,
         end_seconds=min( packing_window.end_seconds, wait_pack_end_seconds ) )
   elif not pack_open_soft_pins_with_free_loops:
      packing_window = _packing_window_with_active_soft_pin_tail_reserve(
         packing_window,
         schedule_window=schedule_window,
         remaining_units=remaining_units,
         active_soft_pin_loop_ids=active_soft_pin_loop_ids,
         hard_pinned_loop_ids=hard_pinned_loop_ids,
         pinned_earliest_start_cache=pinned_earliest_start_cache,
         cursor_seconds=window_state.cursor_seconds )

   packed_units = pack_loops_into_schedule_window(
      walk_graph,
      packing_window,
      prepared_units=_units_excluding_pinned_loops(
         remaining_units,
         packing_hold_loop_ids ),
      cursor_seconds=window_state.cursor_seconds,
      current_node_id=window_state.current_node_id,
      departure_side_cluster_id=window_state.departure_side_cluster_id )
   free_pack_moved_past_open = False

   if packed_units:
      # Right-align against an upcoming soft-pin open (wait-filler) or hard-pin
      # weave deadline so Zoomobile sits beside Face Painting and Face Painting
      # beside Giraffe. Soft-pin-only day-end tail reserves stay left-aligned.
      right_align_to_window_end = (
         packing_window.end_seconds < schedule_window.end_seconds
         and (
               wait_filler_pending
               or hard_pin_deadline_seconds is not None ) )
      window_state.cursor_seconds = _schedule_start_seconds_for_packed_units(
         packing_window,
         packed_units=packed_units,
         cursor_seconds=window_state.cursor_seconds,
         walk_graph=walk_graph,
         current_node_id=window_state.current_node_id,
         right_align_to_window_end=right_align_to_window_end )

      if (
            active_open_seconds is not None
            and window_state.cursor_seconds > active_open_seconds ):
         free_pack_moved_past_open = True

      for prepared_unit in packed_units:
         approach_seconds = approach_travel_seconds_to_unit(
            walk_graph,
            window_state.current_node_id,
            prepared_unit.unit )
         unit_start_seconds = window_state.cursor_seconds + approach_seconds

         if (
               unit_start_seconds + prepared_unit.occupied_seconds
               > packing_window.end_seconds ):
            break

         try:
            unscheduled_animals = _schedule_prepared_loop_unit(
               conn,
               prepared_unit,
               blockers=blockers,
               start_seconds=unit_start_seconds,
               end_seconds=packing_window.end_seconds,
               hours_by_attraction_name=hours_by_attraction_name,
               slot_sink=slot_sink,
               walk_graph=walk_graph )
         except LoopUnitSchedulePersistError as error:
            remaining_animals.extend( error.stops )
            remaining_animals.extend(
               _animals_from_prepared_units( remaining_units ) )
            return False

         remaining_animals.extend( unscheduled_animals )

         if unscheduled_animals:
            continue

         remove_matching_prepared_loop_unit( remaining_units, prepared_unit )
         window_state.cursor_seconds = (
            unit_start_seconds + prepared_unit.occupied_seconds )

         if (
               active_open_seconds is not None
               and window_state.cursor_seconds > active_open_seconds ):
            free_pack_moved_past_open = True

         if prepared_unit.unit.exit_walk_node_id is not None:
            window_state.current_node_id = prepared_unit.unit.exit_walk_node_id

         window_state.departure_side_cluster_id = prepared_unit.unit.side_cluster_id

         if hard_pinned_loop_ids and not wait_filler_pending:
            window_state.cursor_seconds = _drain_ready_pinned_loop_units(
               conn,
               remaining_units,
               schedule_window,
               pinned_earliest_start_cache=pinned_earliest_start_cache,
               blockers=blockers,
               cursor_seconds=window_state.cursor_seconds,
               slot_sink=slot_sink )

         # Soft pins drain after the free-pack wave only when they were held out
         # of packing. Mid-loop late-place was jumping the cursor to window end
         # and then scheduling the rest of packed_units past zoo close.

   if hard_pinned_loop_ids and not wait_filler_pending:
      window_state.cursor_seconds = _drain_ready_pinned_loop_units(
         conn,
         remaining_units,
         schedule_window,
         pinned_earliest_start_cache=pinned_earliest_start_cache,
         blockers=blockers,
         cursor_seconds=window_state.cursor_seconds,
         slot_sink=slot_sink )

   if wait_filler_pending:
      cascade_end_seconds = (
         wait_pack_planned_active_start_seconds
         if wait_pack_planned_active_start_seconds is not None
         else active_open_seconds )

      if cascade_end_seconds is not None:
         # Late-place inactive soft pins (Carousel → Zoomobile) against the active
         # soft pin's planned start — with or without a hard pin ahead.
         window_state.cursor_seconds, window_state.current_node_id = (
            _drain_cascaded_inactive_soft_pin_loop_units(
               conn,
               remaining_units,
               schedule_window,
               active_soft_pin_loop_ids=active_soft_pin_loop_ids,
               hard_pinned_loop_ids=hard_pinned_loop_ids,
               pinned_earliest_start_cache=pinned_earliest_start_cache,
               blockers=blockers,
               cursor_seconds=window_state.cursor_seconds,
               current_node_id=window_state.current_node_id,
               walk_graph=walk_graph,
               cascade_end_seconds=cascade_end_seconds,
               slot_sink=slot_sink ) )

      if hard_pin_deadline_seconds is None:
         window_state.cursor_seconds, window_state.current_node_id = (
            _drain_ready_soft_pin_loop_units(
               conn,
               remaining_units,
               schedule_window,
               soft_only_loop_ids=active_soft_pin_loop_ids - hard_pinned_loop_ids,
               hard_pinned_loop_ids=hard_pinned_loop_ids,
               pinned_earliest_start_cache=pinned_earliest_start_cache,
               blockers=blockers,
               cursor_seconds=window_state.cursor_seconds,
               current_node_id=window_state.current_node_id,
               walk_graph=walk_graph,
               late_place=False,
               slot_sink=slot_sink ) )
      elif (
            active_open_seconds is not None
            and window_state.cursor_seconds >= active_open_seconds ):
         # Free pack may have jumped into the cascade slot. Late-place the active
         # soft pin against the hard pin before the next iteration's hard-pin
         # drain steals the weave window.
         window_state.cursor_seconds, window_state.current_node_id = (
            _drain_ready_soft_pin_loop_units(
               conn,
               remaining_units,
               schedule_window,
               soft_only_loop_ids=active_soft_pin_loop_ids - hard_pinned_loop_ids,
               hard_pinned_loop_ids=hard_pinned_loop_ids,
               pinned_earliest_start_cache=pinned_earliest_start_cache,
               blockers=blockers,
               cursor_seconds=window_state.cursor_seconds,
               current_node_id=window_state.current_node_id,
               walk_graph=walk_graph,
               late_place=True,
               window_end_seconds=hard_pin_deadline_seconds,
               slot_sink=slot_sink ) )

      # Still before open and the active soft pin remains: wait for open / ready.
      if _units_matching_loop_ids(
            remaining_units,
            active_soft_pin_loop_ids ):
         return True

      return True

   if active_soft_pin_loop_ids and not pack_open_soft_pins_with_free_loops:
      late_place = (
         hard_pin_deadline_seconds is not None
         or free_pack_moved_past_open
         or (
               active_open_seconds is not None
               and window_state.cursor_seconds > active_open_seconds ) )
      soft_pin_window_end_seconds = (
         hard_pin_deadline_seconds
         if hard_pin_deadline_seconds is not None
         else schedule_window.end_seconds )
      window_state.cursor_seconds, window_state.current_node_id = (
         _drain_ready_soft_pin_loop_units(
            conn,
            remaining_units,
            schedule_window,
            soft_only_loop_ids=active_soft_pin_loop_ids - hard_pinned_loop_ids,
            hard_pinned_loop_ids=hard_pinned_loop_ids,
            pinned_earliest_start_cache=pinned_earliest_start_cache,
            blockers=blockers,
            cursor_seconds=window_state.cursor_seconds,
            current_node_id=window_state.current_node_id,
            walk_graph=walk_graph,
            late_place=late_place,
            window_end_seconds=soft_pin_window_end_seconds,
            slot_sink=slot_sink ) )

   return True


def _remaining_soft_pins_in_window(
      schedule_window: ItineraryScheduleWindow,
      remaining_units: list[ PreparedLoopScheduleUnit ],
   ) -> list[ AttractionHoursSoftPin ]:
   remaining_loop_ids = {
      prepared_unit.unit.loop_id
      for prepared_unit in remaining_units
      if prepared_unit.unit.loop_id is not None
   }

   return [
      soft_pin
      for soft_pin in schedule_window.attraction_hours_soft_pins
      if soft_pin.loop_id in remaining_loop_ids
   ]


def _active_soft_pin_loop_ids(
      remaining_soft_pins: list[ AttractionHoursSoftPin ],
   ) -> set[ str ]:
   """Activate the tightest remaining hours window (and identical windows)."""
   if not remaining_soft_pins:
      return set()

   ordered = sorted(
      remaining_soft_pins,
      key=lambda soft_pin: (
         soft_pin.close_seconds - soft_pin.open_seconds,
         soft_pin.open_seconds,
         soft_pin.attraction_name ) )
   tightest = ordered[ 0 ]

   return {
      soft_pin.loop_id
      for soft_pin in ordered
      if (
            soft_pin.open_seconds == tightest.open_seconds
            and soft_pin.close_seconds == tightest.close_seconds )
   }


def _earliest_active_soft_pin_open_seconds(
      schedule_window: ItineraryScheduleWindow,
      active_soft_pin_loop_ids: set[ str ],
   ) -> int | None:
   open_seconds = [
      soft_pin.open_seconds
      for soft_pin in schedule_window.attraction_hours_soft_pins
      if soft_pin.loop_id in active_soft_pin_loop_ids
   ]

   if not open_seconds:
      return None

   return min( open_seconds )


def _wait_filler_pack_end_seconds(
      schedule_window: ItineraryScheduleWindow,
      *,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      active_soft_pin_loop_ids: set[ str ],
      hard_pinned_loop_ids: set[ str ],
      active_open_seconds: int,
      hard_pin_deadline_seconds: int | None,
      cursor_seconds: int,
   ) -> tuple[ int, int ]:
   """Return (free-pack end, planned active soft-pin start) for wait-fill cascade.

   Reserves the active soft pin's late-place slot (against a hard pin when
   present) plus inactive soft pins that open before it — including ones already
   open that will late-place after the free pack (Carousel, Zoomobile).
   """
   inactive_before_active_loop_ids = _inactive_soft_pin_loop_ids_before_active(
      schedule_window,
      remaining_units,
      active_soft_pin_loop_ids=active_soft_pin_loop_ids,
      active_open_seconds=active_open_seconds )
   inactive_reserve_seconds = sum(
      prepared_unit.occupied_seconds
      for prepared_unit in _units_matching_loop_ids(
         remaining_units,
         inactive_before_active_loop_ids - hard_pinned_loop_ids ) )

   if hard_pin_deadline_seconds is None:
      planned_active_start_seconds = active_open_seconds
      return (
         max( cursor_seconds, planned_active_start_seconds - inactive_reserve_seconds ),
         planned_active_start_seconds )

   active_soft_occupied_seconds = sum(
      prepared_unit.occupied_seconds
      for prepared_unit in _units_matching_loop_ids(
         remaining_units,
         active_soft_pin_loop_ids - hard_pinned_loop_ids ) )
   planned_active_start_seconds = max(
      active_open_seconds,
      hard_pin_deadline_seconds - active_soft_occupied_seconds )

   return (
      max(
         cursor_seconds,
         planned_active_start_seconds - inactive_reserve_seconds ),
      planned_active_start_seconds )


def _inactive_soft_pin_loop_ids_before_active(
      schedule_window: ItineraryScheduleWindow,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      *,
      active_soft_pin_loop_ids: set[ str ],
      active_open_seconds: int,
   ) -> set[ str ]:
   """Inactive soft pins that open before the active pin (already open or not)."""
   remaining_loop_ids = {
      prepared_unit.unit.loop_id
      for prepared_unit in remaining_units
      if prepared_unit.unit.loop_id is not None
   }

   return {
      soft_pin.loop_id
      for soft_pin in schedule_window.attraction_hours_soft_pins
      if (
            soft_pin.loop_id in remaining_loop_ids
            and soft_pin.loop_id not in active_soft_pin_loop_ids
            and soft_pin.open_seconds < active_open_seconds )
   }


def _drain_cascaded_inactive_soft_pin_loop_units(
      conn: Connection,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      schedule_window: ItineraryScheduleWindow,
      *,
      active_soft_pin_loop_ids: set[ str ],
      hard_pinned_loop_ids: set[ str ],
      pinned_earliest_start_cache: dict[ int, int | None ],
      blockers: list[ TimeBlock ],
      cursor_seconds: int,
      current_node_id: str,
      walk_graph: WalkGraph,
      cascade_end_seconds: int,
      slot_sink: LoopScheduleSlotSink | None = None,
   ) -> tuple[ int, str ]:
   """Late-place inactive soft pins against a cascade deadline (latest open first).

   Zoomobile packs against Face Painting's start, then Carousel against
   Zoomobile's start — so the morning chain stays contiguous.
   """
   active_open_seconds = _earliest_active_soft_pin_open_seconds(
      schedule_window,
      active_soft_pin_loop_ids )

   if active_open_seconds is None:
      return cursor_seconds, current_node_id

   inactive_pins = [
      soft_pin
      for soft_pin in schedule_window.attraction_hours_soft_pins
      if (
            soft_pin.loop_id not in active_soft_pin_loop_ids
            and soft_pin.loop_id not in hard_pinned_loop_ids
            and soft_pin.open_seconds < active_open_seconds )
   ]
   inactive_pins.sort(
      key=lambda soft_pin: ( soft_pin.open_seconds, soft_pin.attraction_name ),
      reverse=True )

   schedule_cursor_seconds = cursor_seconds
   cascade_end = cascade_end_seconds
   placed_end_seconds = cursor_seconds
   resolved_current_node_id = current_node_id

   for soft_pin in inactive_pins:
      matching_units = _units_matching_loop_ids(
         remaining_units,
         { soft_pin.loop_id } )

      if not matching_units:
         continue

      prepared_unit = matching_units[ 0 ]
      drain_cursor_seconds = max( cursor_seconds, soft_pin.open_seconds )

      if not _pinned_loop_is_ready(
            prepared_unit,
            pinned_earliest_start_cache=pinned_earliest_start_cache,
            cursor_seconds=drain_cursor_seconds ):
         continue

      unit_occupied_seconds = prepared_unit.occupied_seconds
      new_cursor_seconds, resolved_current_node_id = (
         _drain_ready_soft_pin_loop_units(
            conn,
            remaining_units,
            schedule_window,
            soft_only_loop_ids={ soft_pin.loop_id },
            hard_pinned_loop_ids=hard_pinned_loop_ids,
            pinned_earliest_start_cache=pinned_earliest_start_cache,
            blockers=blockers,
            cursor_seconds=drain_cursor_seconds,
            current_node_id=resolved_current_node_id,
            walk_graph=walk_graph,
            late_place=True,
            window_end_seconds=cascade_end,
            slot_sink=slot_sink ) )

      if not _units_matching_loop_ids( remaining_units, { soft_pin.loop_id } ):
         cascade_end = cascade_end - unit_occupied_seconds
         placed_end_seconds = max( placed_end_seconds, new_cursor_seconds )

   return (
      max( schedule_cursor_seconds, placed_end_seconds ),
      resolved_current_node_id )


def _inactive_soft_pin_loop_ids_opening_before_active(
      schedule_window: ItineraryScheduleWindow,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      *,
      active_soft_pin_loop_ids: set[ str ],
      cursor_seconds: int,
   ) -> set[ str ]:
   """Inactive soft pins that open after the cursor but before the active pin."""
   active_open_seconds = _earliest_active_soft_pin_open_seconds(
      schedule_window,
      active_soft_pin_loop_ids )

   if active_open_seconds is None:
      return set()

   remaining_loop_ids = {
      prepared_unit.unit.loop_id
      for prepared_unit in remaining_units
      if prepared_unit.unit.loop_id is not None
   }

   return {
      soft_pin.loop_id
      for soft_pin in schedule_window.attraction_hours_soft_pins
      if (
            soft_pin.loop_id in remaining_loop_ids
            and soft_pin.loop_id not in active_soft_pin_loop_ids
            and cursor_seconds < soft_pin.open_seconds < active_open_seconds )
   }


def _packing_window_with_active_soft_pin_tail_reserve(
      packing_window: ItineraryScheduleWindow,
      *,
      schedule_window: ItineraryScheduleWindow,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      active_soft_pin_loop_ids: set[ str ],
      hard_pinned_loop_ids: set[ str ],
      pinned_earliest_start_cache: dict[ int, int | None ],
      cursor_seconds: int,
   ) -> ItineraryScheduleWindow:
   """Reserve the active soft pin at the end of the free-pack window."""
   soft_only_loop_ids = active_soft_pin_loop_ids - hard_pinned_loop_ids

   if not soft_only_loop_ids:
      return packing_window

   active_units = _units_matching_loop_ids( remaining_units, soft_only_loop_ids )

   if not active_units:
      return packing_window

   soft_occupied_seconds = sum(
      prepared_unit.occupied_seconds
      for prepared_unit in active_units )
   soft_pins_by_loop_id = {
      soft_pin.loop_id: soft_pin
      for soft_pin in schedule_window.attraction_hours_soft_pins
      if soft_pin.loop_id in soft_only_loop_ids
   }
   earliest_close_seconds = min(
      (
         soft_pins_by_loop_id[ prepared_unit.unit.loop_id ].close_seconds
         for prepared_unit in active_units
         if prepared_unit.unit.loop_id in soft_pins_by_loop_id
      ),
      default=packing_window.end_seconds )
   hard_pin_start_seconds = _earliest_pinned_loop_wait_seconds(
      remaining_units,
      hard_pinned_loop_ids,
      pinned_earliest_start_cache=pinned_earliest_start_cache,
      cursor_seconds=cursor_seconds )
   soft_pin_deadline_seconds = min(
      packing_window.end_seconds,
      earliest_close_seconds,
      schedule_window.end_seconds )

   if hard_pin_start_seconds is not None:
      soft_pin_deadline_seconds = min(
         soft_pin_deadline_seconds,
         hard_pin_start_seconds )

   reserved_end_seconds = soft_pin_deadline_seconds - soft_occupied_seconds

   if reserved_end_seconds <= cursor_seconds:
      return packing_window

   return replace(
      packing_window,
      end_seconds=min( packing_window.end_seconds, reserved_end_seconds ) )


def _units_matching_loop_ids(
      prepared_units: list[ PreparedLoopScheduleUnit ],
      loop_ids: set[ str ],
   ) -> list[ PreparedLoopScheduleUnit ]:
   if not loop_ids:
      return []

   return [
      prepared_unit
      for prepared_unit in prepared_units
      if prepared_unit.unit.loop_id in loop_ids
   ]


def _should_defer_free_packing_until_after_anchor(
      schedule_window: ItineraryScheduleWindow,
      *,
      later_schedule_windows: list[ ItineraryScheduleWindow ],
      remaining_units: list[ PreparedLoopScheduleUnit ],
      held_pinned_loop_ids: set[ str ],
      pinned_earliest_start_cache: dict[ int, int | None ],
      cursor_seconds: int ) -> bool:
   """Prefer a later post-event gap when free loops fully fit there.

   Morning packing against an upcoming fixed event is skipped when those same
   non-pinned loops can fill the gap after that event before a later pin.
   """
   if schedule_window.opens_after_fixed_time_stop:
      return False

   if schedule_window.anchor_stop is None:
      return False

   anchor_end_seconds = DateValues.time_value_in_seconds(
      schedule_window.anchor_stop.end_time )

   if anchor_end_seconds is None:
      return False

   free_units = _units_excluding_pinned_loops(
      remaining_units,
      held_pinned_loop_ids )

   if not free_units:
      return False

   free_occupied_seconds = sum(
      prepared_unit.occupied_seconds
      for prepared_unit in free_units )

   for later_window in later_schedule_windows:
      if later_window.start_seconds != anchor_end_seconds:
         continue

      if not later_window.opens_after_fixed_time_stop:
         continue

      if not later_window.loop_pins:
         continue

      gap_start_seconds = max( cursor_seconds, later_window.start_seconds )
      reserved_start_seconds = _earliest_pinned_loop_wait_seconds(
         remaining_units,
         {
            loop_pin.loop_id
            for loop_pin in later_window.loop_pins
         },
         pinned_earliest_start_cache=pinned_earliest_start_cache,
         cursor_seconds=gap_start_seconds )

      if reserved_start_seconds is None:
         continue

      return (
         gap_start_seconds + free_occupied_seconds <= reserved_start_seconds )

   return False


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
      exclude_loop_ids: set[ str ] | None = None,
      pinned_earliest_start_cache: dict[ int, int | None ],
      hours_by_attraction_name: dict[ str, OperatingHours ],
      blockers: list[ TimeBlock ],
      walk_graph: WalkGraph,
      window_state: _LoopScheduleWindowState,
      remaining_animals: list[ LoopScheduleStop ],
      slot_sink: LoopScheduleSlotSink | None = None,
   ) -> tuple[ int, bool ]:
   held_loop_ids = set( exclude_loop_ids or pinned_loop_ids )
   held_loop_ids |= pinned_loop_ids

   if schedule_window.opens_after_fixed_time_stop:
      held_loop_ids |= _side_cluster_successor_loop_ids(
         remaining_units,
         pinned_loop_ids )

   non_pinned_units = _units_excluding_pinned_loops(
      remaining_units,
      held_loop_ids )

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

   occupied_seconds = packed_units_occupied_seconds(
      walk_graph,
      packed_units,
      from_node_id=window_state.current_node_id )

   if schedule_window.opens_after_fixed_time_stop:
      schedule_cursor_seconds = window_start_seconds
      next_cursor_seconds = window_start_seconds + occupied_seconds
   else:
      schedule_cursor_seconds = pinned_deadline_seconds - occupied_seconds
      next_cursor_seconds = pinned_deadline_seconds

   for prepared_unit in packed_units:
      approach_seconds = approach_travel_seconds_to_unit(
         walk_graph,
         window_state.current_node_id,
         prepared_unit.unit )
      unit_start_seconds = schedule_cursor_seconds + approach_seconds

      try:
         unscheduled_animals = _schedule_prepared_loop_unit(
            conn,
            prepared_unit,
            blockers=blockers,
            start_seconds=unit_start_seconds,
            end_seconds=pinned_deadline_seconds,
            hours_by_attraction_name=hours_by_attraction_name,
            slot_sink=slot_sink,
            walk_graph=walk_graph )
      except LoopUnitSchedulePersistError as error:
         remaining_animals.extend( error.stops )
         remaining_animals.extend(
            _animals_from_prepared_units( remaining_units ) )
         return window_state.cursor_seconds, True

      if unscheduled_animals:
         remaining_animals.extend( unscheduled_animals )
         return window_state.cursor_seconds, False

      remove_matching_prepared_loop_unit( remaining_units, prepared_unit )
      schedule_cursor_seconds = (
         unit_start_seconds + prepared_unit.occupied_seconds )

      if prepared_unit.unit.exit_walk_node_id is not None:
         window_state.current_node_id = prepared_unit.unit.exit_walk_node_id

      window_state.departure_side_cluster_id = prepared_unit.unit.side_cluster_id

   return next_cursor_seconds, False


def _build_constrained_earliest_start_cache(
      conn: Connection,
      prepared_units: list[ PreparedLoopScheduleUnit ],
      schedule_windows: list[ ItineraryScheduleWindow ],
   ) -> dict[ int, int | None ]:
   hard_pins = [
      loop_pin
      for schedule_window in schedule_windows
      for loop_pin in schedule_window.loop_pins
   ]
   soft_pins = [
      soft_pin
      for schedule_window in schedule_windows
      for soft_pin in schedule_window.attraction_hours_soft_pins
   ]
   hard_pin_loop_ids = { loop_pin.loop_id for loop_pin in hard_pins }
   soft_pin_loop_ids = { soft_pin.loop_id for soft_pin in soft_pins }

   if not hard_pin_loop_ids and not soft_pin_loop_ids:
      return {}

   cache: dict[ int, int | None ] = {}

   for prepared_unit in prepared_units:
      loop_id = prepared_unit.unit.loop_id

      if loop_id is None:
         continue

      earliest_starts: list[ int ] = []

      if loop_id in hard_pin_loop_ids:
         hard_earliest = pinned_loop_earliest_start_seconds(
            conn,
            prepared_unit,
            hard_pins )

         if hard_earliest is not None:
            earliest_starts.append( hard_earliest )

      if loop_id in soft_pin_loop_ids and loop_id not in hard_pin_loop_ids:
         soft_earliest = attraction_hours_loop_earliest_start_seconds(
            conn,
            prepared_unit,
            soft_pins )

         if soft_earliest is not None:
            earliest_starts.append( soft_earliest )

      if earliest_starts:
         cache[ id( prepared_unit ) ] = max( earliest_starts )

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


def _drain_ready_soft_pin_loop_units(
      conn: Connection,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      schedule_window: ItineraryScheduleWindow,
      *,
      soft_only_loop_ids: set[ str ] | None = None,
      hard_pinned_loop_ids: set[ str ],
      pinned_earliest_start_cache: dict[ int, int | None ],
      blockers: list[ TimeBlock ],
      cursor_seconds: int,
      current_node_id: str,
      walk_graph: WalkGraph,
      late_place: bool = False,
      window_end_seconds: int | None = None,
      slot_sink: LoopScheduleSlotSink | None = None,
   ) -> tuple[ int, str ]:
   if soft_only_loop_ids is None:
      soft_pin_loop_ids = _soft_pin_loop_ids_in_window( schedule_window )
      soft_only_loop_ids = soft_pin_loop_ids - hard_pinned_loop_ids

   schedule_cursor_seconds = cursor_seconds
   resolved_current_node_id = current_node_id
   soft_pin_window_end_seconds = (
      schedule_window.end_seconds
      if window_end_seconds is None
      else min( window_end_seconds, schedule_window.end_seconds ) )

   while True:
      made_progress = False

      for prepared_unit in _ready_pinned_loop_units(
            remaining_units,
            soft_only_loop_ids,
            pinned_earliest_start_cache=pinned_earliest_start_cache,
            cursor_seconds=schedule_cursor_seconds ):
         approach_seconds = 0

         if LoopScheduleStopExtractor.transportations_from( list( prepared_unit.unit.stops ) ):
            approach_seconds = approach_travel_seconds_to_unit(
               walk_graph,
               resolved_current_node_id,
               prepared_unit.unit )
         unscheduled_stops, new_cursor_seconds = (
            schedule_prepared_loop_unit_with_attraction_hours(
               conn,
               prepared_unit,
               schedule_window.attraction_hours_soft_pins,
               blockers=blockers,
               window_start_seconds=schedule_window.start_seconds,
               window_end_seconds=soft_pin_window_end_seconds,
               cursor_seconds=schedule_cursor_seconds + approach_seconds,
               late_place=late_place,
               slot_sink=slot_sink ) )

         if not unscheduled_stops:
            remove_matching_prepared_loop_unit( remaining_units, prepared_unit )
            schedule_cursor_seconds = new_cursor_seconds

            if (
                  approach_seconds
                  and prepared_unit.unit.exit_walk_node_id is not None ):
               resolved_current_node_id = prepared_unit.unit.exit_walk_node_id

            made_progress = True
            continue

         if _keep_partial_soft_pin_loop_progress(
               conn,
               remaining_units,
               prepared_unit,
               unscheduled_stops=unscheduled_stops,
               pinned_earliest_start_cache=pinned_earliest_start_cache,
               soft_pins=schedule_window.attraction_hours_soft_pins ):
            schedule_cursor_seconds = max(
               schedule_cursor_seconds,
               new_cursor_seconds )

            if (
                  approach_seconds
                  and prepared_unit.unit.exit_walk_node_id is not None ):
               resolved_current_node_id = prepared_unit.unit.exit_walk_node_id

            made_progress = True
            break

      if not made_progress:
         break

   return schedule_cursor_seconds, resolved_current_node_id


def _earliest_hard_pin_deadline_seconds(
      remaining_units: list[ PreparedLoopScheduleUnit ],
      hard_pinned_loop_ids: set[ str ],
      *,
      pinned_earliest_start_cache: dict[ int, int | None ],
   ) -> int | None:
   if not hard_pinned_loop_ids:
      return None

   deadlines = [
      pinned_earliest_start_cache[ id( prepared_unit ) ]
      for prepared_unit in remaining_units
      if (
            prepared_unit.unit.loop_id in hard_pinned_loop_ids
            and id( prepared_unit ) in pinned_earliest_start_cache
            and pinned_earliest_start_cache[ id( prepared_unit ) ] is not None )
   ]

   if not deadlines:
      return None

   return min( deadlines )

def _keep_partial_pinned_loop_progress(
      conn: Connection,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      prepared_unit: PreparedLoopScheduleUnit,
      *,
      unscheduled_animals: list[ LoopScheduleStop ],
      pinned_earliest_start_cache: dict[ int, int | None ],
      loop_pins: list[ LoopSchedulePin ],
   ) -> bool:
   original_animals = prepared_unit.unit.stops

   if len( unscheduled_animals ) >= len( original_animals ):
      return False

   replacement = _prepared_loop_unit_from_stops(
      conn,
      prepared_unit.unit,
      unscheduled_animals )

   if replacement is None:
      return False

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


def _keep_partial_soft_pin_loop_progress(
      conn: Connection,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      prepared_unit: PreparedLoopScheduleUnit,
      *,
      unscheduled_stops: list[ LoopScheduleStop ],
      pinned_earliest_start_cache: dict[ int, int | None ],
      soft_pins: list[ AttractionHoursSoftPin ],
   ) -> bool:
   original_stops = prepared_unit.unit.stops

   if len( unscheduled_stops ) >= len( original_stops ):
      return False

   replacement = _prepared_loop_unit_from_stops(
      conn,
      prepared_unit.unit,
      unscheduled_stops )

   if replacement is None:
      return False

   for index, candidate in enumerate( remaining_units ):
      if candidate is not prepared_unit:
         continue

      remaining_units[ index ] = replacement
      pinned_earliest_start_cache.pop( id( prepared_unit ), None )
      pinned_earliest_start_cache[ id( replacement ) ] = (
         attraction_hours_loop_earliest_start_seconds(
            conn,
            replacement,
            soft_pins ) )
      return True

   return False


def _prepared_loop_unit_from_stops(
      conn: Connection,
      loop_unit: LoopScheduleUnit,
      stops: list[ LoopScheduleStop ] ) -> PreparedLoopScheduleUnit | None:
   prepared_stops = prepare_loop_schedule_stops(
      conn,
      load_walk_graph(),
      stops )

   if prepared_stops is None:
      return None

   return PreparedLoopScheduleUnit(
      unit=replace( loop_unit, stops=stops ),
      occupied_seconds=total_occupied_seconds( prepared_stops ) )


def _pinned_loop_ids_in_window(
      schedule_window: ItineraryScheduleWindow ) -> set[ str ]:
   return {
      loop_pin.loop_id
      for loop_pin in schedule_window.loop_pins
   }


def _soft_pin_loop_ids_in_window(
      schedule_window: ItineraryScheduleWindow ) -> set[ str ]:
   return {
      soft_pin.loop_id
      for soft_pin in schedule_window.attraction_hours_soft_pins
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


def _side_cluster_successor_loop_ids(
      prepared_units: list[ PreparedLoopScheduleUnit ],
      pinned_loop_ids: set[ str ],
   ) -> set[ str ]:
   """Hold the next same-cluster loop until a pinned neighbor finishes.

   Forward south-cluster order is savanna then giraffe. After a fixed event,
   with a savanna pin, giraffe should follow Warthog instead of packing in the
   pre-pin gap. Morning right-align before the first pin still allows giraffe.
   """
   successor_loop_ids: set[ str ] = set()

   for prepared_unit in prepared_units:
      loop_id = prepared_unit.unit.loop_id
      side_cluster_id = prepared_unit.unit.side_cluster_id
      loop_index = prepared_unit.unit.loop_index_in_side_cluster

      if (
            loop_id is None
            or loop_id not in pinned_loop_ids
            or side_cluster_id is None
            or loop_index is None ):
         continue

      successor_index = loop_index + 1

      for candidate in prepared_units:
         if (
               candidate.unit.side_cluster_id == side_cluster_id
               and candidate.unit.loop_index_in_side_cluster == successor_index
               and candidate.unit.loop_id is not None ):
            successor_loop_ids.add( candidate.unit.loop_id )

   return successor_loop_ids


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


def _should_pack_open_soft_pins_with_free_loops(
      *,
      remaining_units: list[ PreparedLoopScheduleUnit ],
      active_soft_pin_loop_ids: set[ str ],
      held_constrained_loop_ids: set[ str ],
      wait_filler_pending: bool,
      hard_pin_deadline_seconds: int | None,
      active_open_seconds: int | None,
      cursor_seconds: int,
   ) -> bool:
   """Pack already-open soft pins with free loops when no wait-filler or hard pin."""
   if (
         not active_soft_pin_loop_ids
         or wait_filler_pending
         or hard_pin_deadline_seconds is not None
         or active_open_seconds is None
         or cursor_seconds < active_open_seconds ):
      return False

   return any(
      prepared_unit.unit.loop_id is not None
      and prepared_unit.unit.loop_id not in held_constrained_loop_ids
      for prepared_unit in remaining_units )


def _later_same_cluster_loop_ids(
      prepared_units: list[ PreparedLoopScheduleUnit ],
      soft_pin_loop_ids: set[ str ],
   ) -> set[ str ]:
   """Loops later on the same side cluster as an active soft pin.

   Greenhouse sits after Australasia on north. Packing it in the wait before
   Walk-Thru open leaves arrival→Indo dead space and splits the camel corridor.
   """
   if not soft_pin_loop_ids:
      return set()

   later_loop_ids: set[ str ] = set()

   for soft_pin_unit in _units_matching_loop_ids( prepared_units, soft_pin_loop_ids ):
      soft_cluster_id = soft_pin_unit.unit.side_cluster_id
      soft_index = soft_pin_unit.unit.loop_index_in_side_cluster

      if soft_cluster_id is None or soft_index is None:
         continue

      for candidate in prepared_units:
         candidate_loop_id = candidate.unit.loop_id
         candidate_index = candidate.unit.loop_index_in_side_cluster

         if (
               candidate_loop_id is None
               or candidate_loop_id in soft_pin_loop_ids
               or candidate.unit.side_cluster_id != soft_cluster_id
               or candidate_index is None
               or candidate_index <= soft_index ):
            continue

         later_loop_ids.add( candidate_loop_id )

   return later_loop_ids


def _schedule_start_seconds_for_packed_units(
      schedule_window: ItineraryScheduleWindow,
      *,
      packed_units: list[ PreparedLoopScheduleUnit ],
      cursor_seconds: int,
      walk_graph: WalkGraph,
      current_node_id: str,
      right_align_to_window_end: bool = False ) -> int:
   window_start_seconds = _packed_units_start_seconds(
      schedule_window,
      cursor_seconds=cursor_seconds )

   # Hard-pin callers pass right_align_to_window_end. At the *start* of a
   # pre-event window, right-align toward the fixed talk/encounter. Once the
   # cursor has already moved (soft pin placed, etc.), left-align so the next
   # free loops stay contiguous instead of jumping to the event.
   should_right_align = right_align_to_window_end or (
         schedule_window.anchor_stop is not None
         and not schedule_window.opens_after_fixed_time_stop
         and cursor_seconds <= schedule_window.start_seconds )

   if not should_right_align:
      return window_start_seconds

   occupied_seconds = packed_units_occupied_seconds(
      walk_graph,
      packed_units,
      from_node_id=current_node_id )

   return max(
      window_start_seconds,
      schedule_window.end_seconds - occupied_seconds )


def _schedule_prepared_loop_unit(
      conn: Connection,
      prepared_unit: PreparedLoopScheduleUnit,
      *,
      blockers: list[ TimeBlock ],
      start_seconds: int,
      walk_graph: WalkGraph,
      end_seconds: int | None = None,
      hours_by_attraction_name: dict[ str, OperatingHours ] | None = None,
      slot_sink: LoopScheduleSlotSink | None = None ) -> list[ LoopScheduleStop ]:
   animals = list( prepared_unit.unit.stops )
   prepared_stops = prepare_loop_schedule_stops(
      conn,
      walk_graph,
      animals )

   if prepared_stops is None:
      return animals

   if (
         end_seconds is not None
         and start_seconds + total_occupied_seconds( prepared_stops ) > end_seconds ):
      return animals

   animal_slots, slot_end_seconds = (
      assign_contiguous_slots_respecting_attraction_hours(
         prepared_stops,
         start_seconds=start_seconds,
         hours_by_attraction_name=hours_by_attraction_name ) )

   if not animal_slots:
      return animals

   if end_seconds is not None and slot_end_seconds > end_seconds:
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
      loop_units: list[ LoopScheduleUnit ] ) -> list[ LoopScheduleStop ]:
   return [
      animal_row
      for loop_unit in loop_units
      for animal_row in loop_unit.stops
   ]


def _animals_from_prepared_units(
      prepared_units: list[ PreparedLoopScheduleUnit ] ) -> list[
         ItineraryAnimalRecord,
   ]:
   return [
      animal_row
      for prepared_unit in prepared_units
      for animal_row in prepared_unit.unit.stops
   ]
