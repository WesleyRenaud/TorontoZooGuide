from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from ..core.time_block import time_block_from_schedule_times
from ..core.time_block import TimeBlock
from ...data_access.itinerary import fetch_itinerary_date
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_default_duration import fetch_attraction_default_duration_seconds
from ...data_access.itinerary_default_duration import fetch_enclosure_viewing_default_duration_seconds
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ...data_access.schedule_itinerary_item import update_itinerary_animal_schedule
from ...data_access.schedule_itinerary_item import update_itinerary_attraction_schedule
from ...data_access.schedule_itinerary_transportation import apply_itinerary_transportation_schedule
from .loop_schedule_stop import LoopScheduleStop
from .loop_unit_travel_time import inter_stop_travel_seconds
from ....shared.calendar_dates import DateValues
from .timed_loop_schedule_stop import TimedLoopScheduleStop
from ...transportation.default_duration_seconds import default_duration_seconds_for_transportation
from ...transportation.resolve_transportation_day_loop import fetch_transportation_day_loop
from ....types import Connection
from ....types import ScheduleTimeKey
from ....walk_graph.domain.walk_graph import WalkGraph
from ....walk_graph.shortest_path import WalkGraphAdjacency


LoopScheduleSlot = tuple[
   LoopScheduleStop,
   ScheduleTimeKey,
   ScheduleTimeKey,
]


@dataclass
class LoopScheduleSlotSink:
   persist: bool = True
   slots: list[ LoopScheduleSlot ] = field( default_factory=list )


   def save(
         self,
         conn: Connection,
         blockers: list[ TimeBlock ],
         stop_slots: list[ LoopScheduleSlot ] ) -> bool:
      self.slots.extend( stop_slots )

      if self.persist and not _persist_loop_group_slots(
            conn,
            stop_slots ):
         return False

      _append_slots_to_blockers( blockers, stop_slots )
      return True


def prepare_loop_schedule_stops(
      conn: Connection,
      walk_graph: WalkGraph,
      stops: list[ LoopScheduleStop ],
      *,
      adjacency: WalkGraphAdjacency | None = None ) -> list[ TimedLoopScheduleStop ] | None:
   travels = inter_stop_travel_seconds(
      walk_graph,
      stops,
      adjacency=adjacency )
   prepared_stops: list[ TimedLoopScheduleStop ] = []

   for stop, travel_before_seconds in zip( stops, travels ):
      duration_seconds = duration_seconds_for_loop_schedule_stop( conn, stop )

      if duration_seconds is None:
         return None

      prepared_stops.append(
         TimedLoopScheduleStop(
            stop=stop,
            duration_seconds=duration_seconds,
            travel_before_seconds=travel_before_seconds ) )

   return prepared_stops


def total_occupied_seconds( stops: list[ TimedLoopScheduleStop ] ) -> int:
   return sum( stop.occupied_seconds() for stop in stops )


def duration_seconds_for_loop_schedule_stop(
      conn: Connection,
      stop: LoopScheduleStop ) -> int | None:
   stored_block = time_block_from_schedule_times(
      stop.start_time,
      stop.end_time )

   if stored_block is not None:
      return stored_block.end_seconds - stored_block.start_seconds

   return default_duration_seconds_for_loop_schedule_stop( conn, stop )


def default_duration_seconds_for_loop_schedule_stop(
      conn: Connection,
      stop: LoopScheduleStop ) -> int | None:
   if isinstance( stop, ItineraryAttractionRecord ):
      return fetch_attraction_default_duration_seconds(
         conn,
         stop.attraction )

   if isinstance( stop, ItineraryTransportationRecord ):
      return default_duration_seconds_for_transportation(
         conn,
         stop.transportation )

   return fetch_enclosure_viewing_default_duration_seconds(
      conn,
      stop.species,
      stop.exhibit,
      stop.enclosure_name )


def assign_contiguous_slots(
      stops: list[ TimedLoopScheduleStop ],
      *,
      start_seconds: int ) -> tuple[ list[ LoopScheduleSlot ], int ]:
   return assign_contiguous_slots_respecting_attraction_hours(
      stops,
      start_seconds=start_seconds,
      hours_by_attraction_name=None )


def assign_contiguous_slots_respecting_attraction_hours(
      stops: list[ TimedLoopScheduleStop ],
      *,
      start_seconds: int,
      hours_by_attraction_name: dict[ str, tuple[ int, int ] ] | None,
   ) -> tuple[ list[ LoopScheduleSlot ], int ]:
   slots: list[ LoopScheduleSlot ] = []
   slot_cursor_seconds = start_seconds

   for timed_stop in stops:
      slot_cursor_seconds += timed_stop.travel_before_seconds

      if (
            hours_by_attraction_name is not None
            and isinstance(
               timed_stop.stop,
               ( ItineraryAttractionRecord, ItineraryTransportationRecord ) ) ):
         attraction_hours = hours_by_attraction_name.get(
            timed_stop.stop.attraction )

         if attraction_hours is not None:
            open_seconds, close_seconds = attraction_hours

            if slot_cursor_seconds < open_seconds:
               slot_cursor_seconds = open_seconds

            if slot_cursor_seconds + timed_stop.duration_seconds > close_seconds:
               return [], start_seconds

      start_time = DateValues.schedule_time_key_from_seconds(
         slot_cursor_seconds )
      end_seconds = slot_cursor_seconds + timed_stop.duration_seconds
      end_time = DateValues.schedule_time_key_from_seconds( end_seconds )

      if start_time is None or end_time is None:
         return [], start_seconds

      slots.append( ( timed_stop.stop, start_time, end_time ) )
      slot_cursor_seconds = end_seconds

   return slots, slot_cursor_seconds


def assign_contiguous_slots_ending_by(
      stops: list[ TimedLoopScheduleStop ],
      *,
      end_seconds: int ) -> tuple[ list[ LoopScheduleSlot ], int ] | None:
   start_seconds = end_seconds - total_occupied_seconds( stops )

   if start_seconds < 0:
      return None

   stop_slots, segment_end_cursor_seconds = assign_contiguous_slots(
      stops,
      start_seconds=start_seconds )

   if segment_end_cursor_seconds > end_seconds:
      return None

   return stop_slots, segment_end_cursor_seconds


def save_loop_slots(
      conn: Connection,
      blockers: list[ TimeBlock ],
      stop_slots: list[ LoopScheduleSlot ],
      *,
      slot_sink: LoopScheduleSlotSink | None = None ) -> bool:
   if slot_sink is None:
      slot_sink = LoopScheduleSlotSink()

   return slot_sink.save( conn, blockers, stop_slots )


def _append_slots_to_blockers(
      blockers: list[ TimeBlock ],
      slots: list[ LoopScheduleSlot ] ) -> None:
   for _, start_time, end_time in slots:
      scheduled_block = time_block_from_schedule_times(
         start_time,
         end_time )

      if scheduled_block is not None:
         blockers.append( scheduled_block )


def _persist_loop_group_slots(
      conn: Connection,
      scheduled_slots: list[ LoopScheduleSlot ] ) -> bool:
   cur = conn.cursor()

   try:
      for stop, start_time, end_time in scheduled_slots:
         if isinstance( stop, ItineraryAttractionRecord ):
            persisted = update_itinerary_attraction_schedule(
               cur,
               name=stop.attraction,
               start_time=start_time,
               end_time=end_time )
         elif isinstance( stop, ItineraryTransportationRecord ):
            visit_date = fetch_itinerary_date( conn )
            parsed_visit_date = DateValues.parse_date_value( visit_date )
            day_loop = (
               fetch_transportation_day_loop(
                  conn,
                  transportation=stop.transportation,
                  target_date=parsed_visit_date )
               if parsed_visit_date is not None
               else None
            )

            if day_loop is None:
               persisted = False
            else:
               persisted = apply_itinerary_transportation_schedule(
                  cur,
                  name=stop.transportation,
                  start_time=start_time,
                  route=day_loop.route,
                  legs=day_loop.legs )
         else:
            persisted = update_itinerary_animal_schedule(
               cur,
               species=stop.species,
               exhibit=stop.exhibit,
               enclosure_name=stop.enclosure_name,
               start_time=start_time,
               end_time=end_time )

         if not persisted:
            conn.rollback()
            return False

      conn.commit()
      return True

   finally:
      cur.close()
