from __future__ import annotations

from ..core.time_block import TimeBlock
from .loop_pin_gap_step import LoopPinGapStep
from .loop_pin_segment_splitter import LoopPinSegmentSplitter
from .loop_pin_stop_segment import LoopPinStopSegment
from .loop_schedule_slot_assigner import LoopScheduleSlotAssigner
from .loop_schedule_slot_sink import LoopScheduleSlotSink
from .loop_schedule_stop import LoopScheduleStop
from .loop_unit_schedule_persist_error import LoopUnitSchedulePersistError
from .prepared_loop_schedule_unit import PreparedLoopScheduleUnit
from ...routing.loop_schedule_pin import LoopSchedulePin
from ....types import Connection
from ....walk_graph.data_access.load_walk_graph import load_walk_graph


class LoopUnitPinScheduler():
   @classmethod
   def schedule(
         cls,
         conn: Connection,
         prepared_unit: PreparedLoopScheduleUnit,
         loop_pins: list[ LoopSchedulePin ],
         *,
         blockers: list[ TimeBlock ],
         window_start_seconds: int,
         window_end_seconds: int,
         cursor_seconds: int,
         slot_sink: LoopScheduleSlotSink | None = None,
      ) -> tuple[ list[ LoopScheduleStop ], int ]:
      loop_id = prepared_unit.unit.loop_id

      if loop_id is None or not loop_pins:
         return list( prepared_unit.unit.stops ), cursor_seconds

      unit_pins = cls.pins_for_unit( loop_id, loop_pins )

      if not unit_pins:
         return list( prepared_unit.unit.stops ), cursor_seconds

      try:
         new_cursor_seconds, still_unscheduled = cls._schedule_animals_around_loop_pins(
            conn,
            prepared_unit,
            unit_pins,
            blockers=blockers,
            window_start_seconds=window_start_seconds,
            window_end_seconds=window_end_seconds,
            cursor_seconds=cursor_seconds,
            slot_sink=slot_sink )
      except LoopUnitSchedulePersistError as error:
         return error.stops, cursor_seconds

      return still_unscheduled, new_cursor_seconds


   @classmethod
   def earliest_start_seconds(
         cls,
         conn: Connection,
         prepared_unit: PreparedLoopScheduleUnit,
         loop_pins: list[ LoopSchedulePin ],
      ) -> int | None:
      loop_id = prepared_unit.unit.loop_id

      if loop_id is None:
         return None

      unit_pins = cls.pins_for_unit( loop_id, loop_pins )

      if not unit_pins:
         return None

      first_pin = unit_pins[ 0 ]
      before_pin_animals = LoopPinSegmentSplitter.animals_before_first_pin(
         list( prepared_unit.unit.stops ),
         loop_id=loop_id,
         loop_pins=unit_pins )

      if not before_pin_animals:
         return first_pin.start_seconds

      prepared_stops = LoopScheduleSlotAssigner.prepare_stops(
         conn,
         load_walk_graph(),
         before_pin_animals )

      if prepared_stops is None:
         return None

      return first_pin.start_seconds - sum(
         timed_stop.duration_seconds
         for timed_stop in prepared_stops )


   @classmethod
   def pins_for_unit(
         cls,
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


   @classmethod
   def _schedule_animals_around_loop_pins(
         cls,
         conn: Connection,
         prepared_unit: PreparedLoopScheduleUnit,
         loop_pins: list[ LoopSchedulePin ],
         *,
         blockers: list[ TimeBlock ],
         window_start_seconds: int,
         window_end_seconds: int,
         cursor_seconds: int,
         slot_sink: LoopScheduleSlotSink | None = None,
      ) -> tuple[ int, list[ LoopScheduleStop ] ]:
      animals = list( prepared_unit.unit.stops )
      loop_id = prepared_unit.unit.loop_id

      if loop_id is None:
         raise LoopUnitSchedulePersistError( animals )

      schedule_steps = LoopPinSegmentSplitter.schedule_steps(
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
               return schedule_cursor_seconds, cls._still_unscheduled_animals(
                  animals,
                  scheduled_animal_ids=scheduled_animal_ids )

            schedule_cursor_seconds = max(
               schedule_cursor_seconds,
               loop_pin.end_seconds )
            continue

         schedule_cursor_seconds = cls._schedule_animal_segment_step(
            conn,
            schedule_step,
            blockers=blockers,
            animals=animals,
            loop_pins=loop_pins,
            schedule_cursor_seconds=schedule_cursor_seconds,
            scheduled_animal_ids=scheduled_animal_ids,
            slot_sink=slot_sink )

      # Before-pin animals skipped when arriving at/after the pin still belong in
      # this pavilion visit — place them contiguously after the woven segments
      # instead of leaving a partial loop that later attractions can split.
      still_unscheduled = cls._still_unscheduled_animals(
         animals,
         scheduled_animal_ids=scheduled_animal_ids )

      if still_unscheduled:
         schedule_cursor_seconds = cls._schedule_remaining_animals_forward(
            conn,
            animals=animals,
            animal_group=still_unscheduled,
            blockers=blockers,
            start_seconds=schedule_cursor_seconds,
            window_end_seconds=window_end_seconds,
            scheduled_animal_ids=scheduled_animal_ids,
            slot_sink=slot_sink )

      if schedule_cursor_seconds > window_end_seconds:
         raise LoopUnitSchedulePersistError( animals )

      return schedule_cursor_seconds, cls._still_unscheduled_animals(
         animals,
         scheduled_animal_ids=scheduled_animal_ids )


   @classmethod
   def _schedule_animal_segment_step(
         cls,
         conn: Connection,
         schedule_step: LoopPinStopSegment,
         *,
         blockers: list[ TimeBlock ],
         animals: list[ LoopScheduleStop ],
         loop_pins: list[ LoopSchedulePin ],
         schedule_cursor_seconds: int,
         scheduled_animal_ids: set[ int ],
         slot_sink: LoopScheduleSlotSink | None = None,
      ) -> int:
      if cls._should_skip_animal_segment_step(
            schedule_step,
            loop_pins=loop_pins,
            schedule_cursor_seconds=schedule_cursor_seconds ):
         return schedule_cursor_seconds

      unscheduled_animals = [
         animal_row
         for animal_row in schedule_step.stops
         if id( animal_row ) not in scheduled_animal_ids
      ]

      if not unscheduled_animals:
         return schedule_cursor_seconds

      segment_end_seconds = cls._schedule_animal_segment(
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


   @classmethod
   def _should_skip_animal_segment_step(
         cls,
         schedule_step: LoopPinStopSegment,
         *,
         loop_pins: list[ LoopSchedulePin ],
         schedule_cursor_seconds: int,
      ) -> bool:
      if schedule_step.anchor_at_end:
         return schedule_cursor_seconds >= schedule_step.end_before_seconds

      if not loop_pins:
         return False

      return schedule_cursor_seconds < loop_pins[ -1 ].end_seconds


   @classmethod
   def _schedule_animal_segment(
         cls,
         conn: Connection,
         *,
         blockers: list[ TimeBlock ],
         animals: list[ LoopScheduleStop ],
         animal_group: list[ LoopScheduleStop ],
         start_seconds: int,
         segment_end_seconds: int,
         backward_anchor: bool,
         slot_sink: LoopScheduleSlotSink | None = None,
      ) -> int:
      prepared_stops = LoopScheduleSlotAssigner.prepare_stops(
         conn,
         load_walk_graph(),
         animal_group )

      if prepared_stops is None:
         raise LoopUnitSchedulePersistError( animals )

      occupied_seconds = LoopScheduleSlotAssigner.total_occupied_seconds( prepared_stops )

      if backward_anchor:
         latest_start_seconds = segment_end_seconds - occupied_seconds

         if latest_start_seconds < start_seconds:
            raise LoopUnitSchedulePersistError( animals )

         slot_assignment = LoopScheduleSlotAssigner.assign_contiguous_ending_by(
            prepared_stops,
            end_seconds=segment_end_seconds )

         if slot_assignment is None:
            raise LoopUnitSchedulePersistError( animals )

         animal_slots, segment_end_cursor_seconds = slot_assignment
         effective_start_seconds = latest_start_seconds
      else:
         if start_seconds >= segment_end_seconds:
            raise LoopUnitSchedulePersistError( animals )

         if start_seconds + occupied_seconds > segment_end_seconds:
            raise LoopUnitSchedulePersistError( animals )

         animal_slots, segment_end_cursor_seconds = LoopScheduleSlotAssigner.assign_contiguous(
            prepared_stops,
            start_seconds=start_seconds )
         effective_start_seconds = start_seconds

      if effective_start_seconds < start_seconds:
         raise LoopUnitSchedulePersistError( animals )

      if not animal_slots:
         raise LoopUnitSchedulePersistError( animals )

      if not LoopScheduleSlotAssigner.save(
            conn,
            blockers,
            animal_slots,
            slot_sink=slot_sink ):
         raise LoopUnitSchedulePersistError( animals )

      return segment_end_cursor_seconds


   @classmethod
   def _schedule_remaining_animals_forward(
         cls,
         conn: Connection,
         *,
         animals: list[ LoopScheduleStop ],
         animal_group: list[ LoopScheduleStop ],
         blockers: list[ TimeBlock ],
         start_seconds: int,
         window_end_seconds: int,
         scheduled_animal_ids: set[ int ],
         slot_sink: LoopScheduleSlotSink | None = None,
      ) -> int:
      prepared_stops = LoopScheduleSlotAssigner.prepare_stops(
         conn,
         load_walk_graph(),
         animal_group )

      if prepared_stops is None:
         raise LoopUnitSchedulePersistError( animals )

      if start_seconds + LoopScheduleSlotAssigner.total_occupied_seconds( prepared_stops ) > window_end_seconds:
         return start_seconds

      animal_slots, segment_end_cursor_seconds = LoopScheduleSlotAssigner.assign_contiguous(
         prepared_stops,
         start_seconds=start_seconds )

      if not animal_slots:
         return start_seconds

      if not LoopScheduleSlotAssigner.save(
            conn,
            blockers,
            animal_slots,
            slot_sink=slot_sink ):
         raise LoopUnitSchedulePersistError( animals )

      scheduled_animal_ids.update( id( animal_row ) for animal_row in animal_group )
      return segment_end_cursor_seconds


   @classmethod
   def _still_unscheduled_animals(
         cls,
         animals: list[ LoopScheduleStop ],
         *,
         scheduled_animal_ids: set[ int ],
      ) -> list[ LoopScheduleStop ]:
      return [
         animal_row
         for animal_row in animals
         if id( animal_row ) not in scheduled_animal_ids
      ]
