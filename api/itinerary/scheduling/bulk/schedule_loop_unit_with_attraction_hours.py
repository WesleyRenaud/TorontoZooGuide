from __future__ import annotations

from .attraction_hours_soft_pin import stops_before_attraction_hours_soft_pin
from ..core.time_block import TimeBlock
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from .loop_schedule_stop import LoopScheduleStop
from .loop_unit_schedule_persist_error import LoopUnitSchedulePersistError
from .loop_unit_schedule_slots import assign_contiguous_slots_ending_by
from .loop_unit_schedule_slots import assign_contiguous_slots_respecting_attraction_hours
from .loop_unit_schedule_slots import duration_seconds_for_loop_schedule_stop
from .loop_unit_schedule_slots import LoopScheduleSlotSink
from .loop_unit_schedule_slots import prepare_loop_schedule_stops
from .loop_unit_schedule_slots import save_loop_slots
from .loop_unit_schedule_slots import total_occupied_seconds
from .pack_loops_into_schedule_window import PreparedLoopScheduleUnit
from ...routing.attraction_hours_soft_pin import AttractionHoursSoftPin
from ....shared.calendar_dates import DateValues
from ....types import Connection
from ....walk_graph.data_access.load_walk_graph import load_walk_graph


def schedule_prepared_loop_unit_with_attraction_hours(
      conn: Connection,
      prepared_unit: PreparedLoopScheduleUnit,
      soft_pins: list[ AttractionHoursSoftPin ],
      *,
      blockers: list[ TimeBlock ],
      window_start_seconds: int,
      window_end_seconds: int,
      cursor_seconds: int,
      late_place: bool = False,
      slot_sink: LoopScheduleSlotSink | None = None,
   ) -> tuple[ list[ LoopScheduleStop ], int ]:
   loop_id = prepared_unit.unit.loop_id

   if loop_id is None or not soft_pins:
      return list( prepared_unit.unit.stops ), cursor_seconds

   unit_soft_pins = unit_attraction_hours_soft_pins( loop_id, soft_pins )

   if not unit_soft_pins:
      return list( prepared_unit.unit.stops ), cursor_seconds

   try:
      new_cursor_seconds, still_unscheduled = _schedule_stops_around_attraction_hours(
         conn,
         prepared_unit,
         unit_soft_pins,
         blockers=blockers,
         window_start_seconds=window_start_seconds,
         window_end_seconds=window_end_seconds,
         cursor_seconds=cursor_seconds,
         late_place=late_place,
         slot_sink=slot_sink )
   except LoopUnitSchedulePersistError as error:
      return error.stops, cursor_seconds

   return still_unscheduled, new_cursor_seconds


def attraction_hours_loop_earliest_start_seconds(
      conn: Connection,
      prepared_unit: PreparedLoopScheduleUnit,
      soft_pins: list[ AttractionHoursSoftPin ],
   ) -> int | None:
   loop_id = prepared_unit.unit.loop_id

   if loop_id is None:
      return None

   unit_soft_pins = unit_attraction_hours_soft_pins( loop_id, soft_pins )

   if not unit_soft_pins:
      return None

   first_soft_pin = unit_soft_pins[ 0 ]
   before_stops = stops_before_attraction_hours_soft_pin(
      list( prepared_unit.unit.stops ),
      loop_id=loop_id,
      soft_pin=first_soft_pin )

   if not before_stops:
      return first_soft_pin.open_seconds

   prepared_stops = prepare_loop_schedule_stops(
      conn,
      load_walk_graph(),
      before_stops )

   if prepared_stops is None:
      return None

   return first_soft_pin.open_seconds - sum(
      timed_stop.duration_seconds
      for timed_stop in prepared_stops )


def unit_attraction_hours_soft_pins(
      loop_id: str,
      soft_pins: list[ AttractionHoursSoftPin ],
   ) -> list[ AttractionHoursSoftPin ]:
   unit_soft_pins = [
      soft_pin
      for soft_pin in soft_pins
      if soft_pin.loop_id == loop_id
   ]
   unit_soft_pins.sort( key=lambda soft_pin: soft_pin.viewing_spot_index )
   return unit_soft_pins


def _schedule_stops_around_attraction_hours(
      conn: Connection,
      prepared_unit: PreparedLoopScheduleUnit,
      soft_pins: list[ AttractionHoursSoftPin ],
      *,
      blockers: list[ TimeBlock ],
      window_start_seconds: int,
      window_end_seconds: int,
      cursor_seconds: int,
      late_place: bool = False,
      slot_sink: LoopScheduleSlotSink | None = None,
   ) -> tuple[ int, list[ LoopScheduleStop ] ]:
   stops = list( prepared_unit.unit.stops )
   loop_id = prepared_unit.unit.loop_id

   if loop_id is None:
      raise LoopUnitSchedulePersistError( stops )

   soft_pin_attraction_names = {
      soft_pin.attraction_name
      for soft_pin in soft_pins
   }
   scheduled_stop_ids: set[ int ] = set()
   schedule_cursor_seconds = max( cursor_seconds, window_start_seconds )

   for soft_pin in soft_pins:
      attraction_stop = _attraction_stop_for_soft_pin( stops, soft_pin )

      if attraction_stop is None:
         return schedule_cursor_seconds, _still_unscheduled_stops(
            stops,
            scheduled_stop_ids=scheduled_stop_ids )

      before_stops = [
         stop
         for stop in stops_before_attraction_hours_soft_pin(
            stops,
            loop_id=loop_id,
            soft_pin=soft_pin )
         if id( stop ) not in scheduled_stop_ids
         and not _stop_is_soft_pinned_attraction( stop, soft_pin_attraction_names )
      ]

      attraction_duration_seconds = _duration_seconds_or_raise(
         conn,
         attraction_stop,
         all_stops=stops )
      attraction_start_seconds = max(
         schedule_cursor_seconds,
         soft_pin.open_seconds )

      if before_stops:
         prepared_before_stops = prepare_loop_schedule_stops(
            conn,
            load_walk_graph(),
            before_stops )

         if prepared_before_stops is None:
            return schedule_cursor_seconds, _still_unscheduled_stops(
               stops,
               scheduled_stop_ids=scheduled_stop_ids )

         before_total_seconds = total_occupied_seconds( prepared_before_stops )
         attraction_start_seconds = max(
            attraction_start_seconds,
            schedule_cursor_seconds + before_total_seconds )
         before_end_seconds = attraction_start_seconds

         if before_end_seconds - before_total_seconds < schedule_cursor_seconds:
            return schedule_cursor_seconds, _still_unscheduled_stops(
               stops,
               scheduled_stop_ids=scheduled_stop_ids )

         slot_assignment = assign_contiguous_slots_ending_by(
            prepared_before_stops,
            end_seconds=before_end_seconds )

         if slot_assignment is None:
            return schedule_cursor_seconds, _still_unscheduled_stops(
               stops,
               scheduled_stop_ids=scheduled_stop_ids )

         before_slots, _ = slot_assignment

         if not save_loop_slots(
               conn,
               blockers,
               before_slots,
               slot_sink=slot_sink ):
            return schedule_cursor_seconds, _still_unscheduled_stops(
               stops,
               scheduled_stop_ids=scheduled_stop_ids )

         scheduled_stop_ids.update( id( stop ) for stop in before_stops )

      elif late_place:
         # Attraction-only soft pin already open: right-align before close /
         # window end instead of locking the first open slot.
         latest_start_seconds = (
            min( soft_pin.close_seconds, window_end_seconds )
            - attraction_duration_seconds )

         if latest_start_seconds >= attraction_start_seconds:
            attraction_start_seconds = latest_start_seconds

      attraction_end_seconds = (
         attraction_start_seconds + attraction_duration_seconds )

      if (
            attraction_end_seconds > soft_pin.close_seconds
            or attraction_end_seconds > window_end_seconds ):
         return schedule_cursor_seconds, _still_unscheduled_stops(
            stops,
            scheduled_stop_ids=scheduled_stop_ids )

      attraction_start_time = DateValues.schedule_time_key_from_seconds(
         attraction_start_seconds )
      attraction_end_time = DateValues.schedule_time_key_from_seconds(
         attraction_end_seconds )

      if attraction_start_time is None or attraction_end_time is None:
         return schedule_cursor_seconds, _still_unscheduled_stops(
            stops,
            scheduled_stop_ids=scheduled_stop_ids )

      if not save_loop_slots(
            conn,
            blockers,
            [ ( attraction_stop, attraction_start_time, attraction_end_time ) ],
            slot_sink=slot_sink ):
         return schedule_cursor_seconds, _still_unscheduled_stops(
            stops,
            scheduled_stop_ids=scheduled_stop_ids )

      scheduled_stop_ids.add( id( attraction_stop ) )
      schedule_cursor_seconds = attraction_end_seconds

   after_stops = [
      stop
      for stop in stops
      if id( stop ) not in scheduled_stop_ids
   ]

   if after_stops:
      prepared_after_stops = prepare_loop_schedule_stops(
         conn,
         load_walk_graph(),
         after_stops )

      if prepared_after_stops is None:
         return schedule_cursor_seconds, _still_unscheduled_stops(
            stops,
            scheduled_stop_ids=scheduled_stop_ids )

      if (
            schedule_cursor_seconds
            + total_occupied_seconds( prepared_after_stops ) > window_end_seconds ):
         return schedule_cursor_seconds, _still_unscheduled_stops(
            stops,
            scheduled_stop_ids=scheduled_stop_ids )

      after_slots, schedule_cursor_seconds = (
         assign_contiguous_slots_respecting_attraction_hours(
            prepared_after_stops,
            start_seconds=schedule_cursor_seconds,
            hours_by_attraction_name={
               soft_pin.attraction_name: (
                  soft_pin.open_seconds,
                  soft_pin.close_seconds )
               for soft_pin in soft_pins
            } ) )

      if not after_slots:
         return schedule_cursor_seconds, _still_unscheduled_stops(
            stops,
            scheduled_stop_ids=scheduled_stop_ids )

      if not save_loop_slots(
            conn,
            blockers,
            after_slots,
            slot_sink=slot_sink ):
         return schedule_cursor_seconds, _still_unscheduled_stops(
            stops,
            scheduled_stop_ids=scheduled_stop_ids )

      scheduled_stop_ids.update( id( stop ) for stop in after_stops )

   if schedule_cursor_seconds > window_end_seconds:
      return schedule_cursor_seconds, _still_unscheduled_stops(
         stops,
         scheduled_stop_ids=scheduled_stop_ids )

   return schedule_cursor_seconds, _still_unscheduled_stops(
      stops,
      scheduled_stop_ids=scheduled_stop_ids )


def _attraction_stop_for_soft_pin(
      stops: list[ LoopScheduleStop ],
      soft_pin: AttractionHoursSoftPin,
   ) -> ItineraryAttractionRecord | None:
   for stop in stops:
      if (
            isinstance( stop, ItineraryAttractionRecord )
            and stop.attraction == soft_pin.attraction_name ):
         return stop

   return None


def _stop_is_soft_pinned_attraction(
      stop: LoopScheduleStop,
      soft_pin_attraction_names: set[ str ],
   ) -> bool:
   return (
      isinstance( stop, ItineraryAttractionRecord )
      and stop.attraction in soft_pin_attraction_names )


def _duration_seconds_or_raise(
      conn: Connection,
      stop: LoopScheduleStop,
      *,
      all_stops: list[ LoopScheduleStop ],
   ) -> int:
   duration_seconds = duration_seconds_for_loop_schedule_stop( conn, stop )

   if duration_seconds is None:
      raise LoopUnitSchedulePersistError( all_stops )

   return duration_seconds


def _still_unscheduled_stops(
      stops: list[ LoopScheduleStop ],
      *,
      scheduled_stop_ids: set[ int ],
   ) -> list[ LoopScheduleStop ]:
   return [
      stop
      for stop in stops
      if id( stop ) not in scheduled_stop_ids
   ]
