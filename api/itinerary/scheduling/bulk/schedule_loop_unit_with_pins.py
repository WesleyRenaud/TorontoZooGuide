from __future__ import annotations

from ..core.time_block import TimeBlock
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from .loop_pin_segments import animals_before_first_loop_pin
from .loop_pin_segments import loop_pin_schedule_steps
from .loop_pin_segments import LoopPinAnimalSegment
from .loop_pin_segments import LoopPinGapStep
from .loop_unit_schedule_persist_error import LoopUnitSchedulePersistError
from .loop_unit_schedule_slots import assign_contiguous_slots
from .loop_unit_schedule_slots import assign_contiguous_slots_ending_by
from .loop_unit_schedule_slots import fetch_viewing_durations
from .loop_unit_schedule_slots import LoopScheduleSlotSink
from .loop_unit_schedule_slots import save_loop_slots
from .pack_loops_into_schedule_window import PreparedLoopScheduleUnit
from ...routing.loop_schedule_pin import LoopSchedulePin
from ....types import Connection


def schedule_prepared_loop_unit_with_pins(
      conn: Connection,
      prepared_unit: PreparedLoopScheduleUnit,
      loop_pins: list[ LoopSchedulePin ],
      *,
      blockers: list[ TimeBlock ],
      window_start_seconds: int,
      window_end_seconds: int,
      cursor_seconds: int,
      slot_sink: LoopScheduleSlotSink | None = None,
   ) -> tuple[ list[ ItineraryAnimalRecord ], int ]:
   loop_id = prepared_unit.unit.loop_id

   if loop_id is None or not loop_pins:
      return list( prepared_unit.unit.animals ), cursor_seconds

   unit_pins = unit_loop_pins( loop_id, loop_pins )

   if not unit_pins:
      return list( prepared_unit.unit.animals ), cursor_seconds

   try:
      new_cursor_seconds, still_unscheduled = _schedule_animals_around_loop_pins(
         conn,
         prepared_unit,
         unit_pins,
         blockers=blockers,
         window_start_seconds=window_start_seconds,
         window_end_seconds=window_end_seconds,
         cursor_seconds=cursor_seconds,
         slot_sink=slot_sink )
   except LoopUnitSchedulePersistError as error:
      return error.animals, cursor_seconds

   return still_unscheduled, new_cursor_seconds


def pinned_loop_earliest_start_seconds(
      conn: Connection,
      prepared_unit: PreparedLoopScheduleUnit,
      loop_pins: list[ LoopSchedulePin ],
   ) -> int | None:
   loop_id = prepared_unit.unit.loop_id

   if loop_id is None:
      return None

   unit_pins = unit_loop_pins( loop_id, loop_pins )

   if not unit_pins:
      return None

   first_pin = unit_pins[ 0 ]
   before_pin_animals = animals_before_first_loop_pin(
      list( prepared_unit.unit.animals ),
      loop_id=loop_id,
      loop_pins=unit_pins )

   if not before_pin_animals:
      return first_pin.start_seconds

   durations = fetch_viewing_durations( conn, before_pin_animals )

   if durations is None:
      return None

   return first_pin.start_seconds - sum( durations )


def unit_loop_pins(
      loop_id: str,
      loop_pins: list[ LoopSchedulePin ],
   ) -> list[ LoopSchedulePin ]:
   unit_pins = [
      loop_pin
      for loop_pin in loop_pins
      if loop_pin.loop_id == loop_id
   ]
   unit_pins.sort( key=lambda loop_pin: loop_pin.start_seconds )

   return unit_pins


def _schedule_animals_around_loop_pins(
      conn: Connection,
      prepared_unit: PreparedLoopScheduleUnit,
      loop_pins: list[ LoopSchedulePin ],
      *,
      blockers: list[ TimeBlock ],
      window_start_seconds: int,
      window_end_seconds: int,
      cursor_seconds: int,
      slot_sink: LoopScheduleSlotSink | None = None,
   ) -> tuple[ int, list[ ItineraryAnimalRecord ] ]:
   animals = list( prepared_unit.unit.animals )
   loop_id = prepared_unit.unit.loop_id

   if loop_id is None:
      raise LoopUnitSchedulePersistError( animals )

   schedule_steps = loop_pin_schedule_steps(
      animals,
      loop_id=loop_id,
      loop_pins=loop_pins,
      window_end_seconds=window_end_seconds )
   schedule_cursor_seconds = max( cursor_seconds, window_start_seconds )
   scheduled_animal_ids: set[ int ] = set()

   for schedule_step in schedule_steps:
      if isinstance( schedule_step, LoopPinGapStep ):
         loop_pin = schedule_step.loop_pin

         if schedule_cursor_seconds >= loop_pin.end_seconds:
            continue

         if loop_pin.end_seconds > window_end_seconds:
            return schedule_cursor_seconds, _still_unscheduled_animals(
               animals,
               scheduled_animal_ids=scheduled_animal_ids )

         schedule_cursor_seconds = max(
            schedule_cursor_seconds,
            loop_pin.end_seconds )
         continue

      schedule_cursor_seconds = _schedule_animal_segment_step(
         conn,
         schedule_step,
         blockers=blockers,
         animals=animals,
         loop_pins=loop_pins,
         schedule_cursor_seconds=schedule_cursor_seconds,
         scheduled_animal_ids=scheduled_animal_ids,
         slot_sink=slot_sink )

   if schedule_cursor_seconds > window_end_seconds:
      raise LoopUnitSchedulePersistError( animals )

   return schedule_cursor_seconds, _still_unscheduled_animals(
      animals,
      scheduled_animal_ids=scheduled_animal_ids )


def _schedule_animal_segment_step(
      conn: Connection,
      schedule_step: LoopPinAnimalSegment,
      *,
      blockers: list[ TimeBlock ],
      animals: list[ ItineraryAnimalRecord ],
      loop_pins: list[ LoopSchedulePin ],
      schedule_cursor_seconds: int,
      scheduled_animal_ids: set[ int ],
      slot_sink: LoopScheduleSlotSink | None = None,
   ) -> int:
   if _should_skip_animal_segment_step(
         schedule_step,
         loop_pins=loop_pins,
         schedule_cursor_seconds=schedule_cursor_seconds ):
      return schedule_cursor_seconds

   unscheduled_animals = [
      animal_row
      for animal_row in schedule_step.animals
      if id( animal_row ) not in scheduled_animal_ids
   ]

   if not unscheduled_animals:
      return schedule_cursor_seconds

   segment_end_seconds = _schedule_animal_segment(
      conn,
      blockers=blockers,
      animals=animals,
      animal_group=unscheduled_animals,
      start_seconds=schedule_cursor_seconds,
      segment_end_seconds=schedule_step.end_before_seconds,
      backward_anchor=schedule_step.anchor_at_end,
      slot_sink=slot_sink )
   scheduled_animal_ids.update(
      id( animal_row )
      for animal_row in unscheduled_animals )

   return segment_end_seconds


def _should_skip_animal_segment_step(
      schedule_step: LoopPinAnimalSegment,
      *,
      loop_pins: list[ LoopSchedulePin ],
      schedule_cursor_seconds: int,
   ) -> bool:
   if schedule_step.anchor_at_end:
      return schedule_cursor_seconds >= schedule_step.end_before_seconds

   if not loop_pins:
      return False

   return schedule_cursor_seconds < loop_pins[ -1 ].end_seconds


def _schedule_animal_segment(
      conn: Connection,
      *,
      blockers: list[ TimeBlock ],
      animals: list[ ItineraryAnimalRecord ],
      animal_group: list[ ItineraryAnimalRecord ],
      start_seconds: int,
      segment_end_seconds: int,
      backward_anchor: bool,
      slot_sink: LoopScheduleSlotSink | None = None,
   ) -> int:
   durations = fetch_viewing_durations( conn, animal_group )

   if durations is None:
      raise LoopUnitSchedulePersistError( animals )

   total_duration_seconds = sum( durations )

   if backward_anchor:
      latest_start_seconds = segment_end_seconds - total_duration_seconds

      if latest_start_seconds < start_seconds:
         raise LoopUnitSchedulePersistError( animals )

      slot_assignment = assign_contiguous_slots_ending_by(
         animal_group,
         durations,
         end_seconds=segment_end_seconds )

      if slot_assignment is None:
         raise LoopUnitSchedulePersistError( animals )

      animal_slots, segment_end_cursor_seconds = slot_assignment
      effective_start_seconds = latest_start_seconds
   else:
      if start_seconds >= segment_end_seconds:
         raise LoopUnitSchedulePersistError( animals )

      if start_seconds + total_duration_seconds > segment_end_seconds:
         raise LoopUnitSchedulePersistError( animals )

      animal_slots, segment_end_cursor_seconds = assign_contiguous_slots(
         animal_group,
         durations,
         start_seconds=start_seconds )
      effective_start_seconds = start_seconds

   if effective_start_seconds < start_seconds:
      raise LoopUnitSchedulePersistError( animals )

   if not animal_slots:
      raise LoopUnitSchedulePersistError( animals )

   if not save_loop_slots(
         conn,
         blockers,
         animal_slots,
         slot_sink=slot_sink ):
      raise LoopUnitSchedulePersistError( animals )

   return segment_end_cursor_seconds


def _still_unscheduled_animals(
      animals: list[ ItineraryAnimalRecord ],
      *,
      scheduled_animal_ids: set[ int ],
   ) -> list[ ItineraryAnimalRecord ]:
   return [
      animal_row
      for animal_row in animals
      if id( animal_row ) not in scheduled_animal_ids
   ]


def viewing_spot_index_for_animal_in_loop(
      loop_id: str,
      animal_row: ItineraryAnimalRecord ) -> int | None:
   from .loop_pin_segments import viewing_spot_index_for_animal_in_loop as lookup

   return lookup( loop_id, animal_row )
