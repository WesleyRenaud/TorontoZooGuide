from __future__ import annotations

from ..core.time_block import TimeBlock
from ..core.time_block_builder import TimeBlockBuilder
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_default_duration_provider import ItineraryDefaultDurationProvider
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord
from .loop_schedule_slot import LoopScheduleSlot
from .loop_schedule_slot_sink import LoopScheduleSlotSink
from .loop_schedule_stop import LoopScheduleStop
from .loop_unit_travel_time_calculator import LoopUnitTravelTimeCalculator
from ....shared.calendar_dates import DateValues
from ....shared.operating_hours import OperatingHours
from .timed_loop_schedule_stop import TimedLoopScheduleStop
from ...transportation.default_duration_seconds import default_duration_seconds_for_transportation
from ....types import Connection
from ....walk_graph.domain.walk_graph import WalkGraph
from ....walk_graph.shortest_path import WalkGraphAdjacency


class LoopScheduleSlotAssigner():
   @classmethod
   def prepare_stops(
         cls,
         conn: Connection,
         walk_graph: WalkGraph,
         stops: list[ LoopScheduleStop ],
         *,
         adjacency: WalkGraphAdjacency | None = None ) -> list[ TimedLoopScheduleStop ] | None:
      travels = LoopUnitTravelTimeCalculator.inter_stop_seconds(
         walk_graph,
         stops,
         adjacency=adjacency )
      prepared_stops: list[ TimedLoopScheduleStop ] = []

      for stop, travel_before_seconds in zip( stops, travels ):
         duration_seconds = cls.duration_seconds_for_stop( conn, stop )

         if duration_seconds is None:
            return None

         prepared_stops.append(
            TimedLoopScheduleStop(
               stop=stop,
               duration_seconds=duration_seconds,
               travel_before_seconds=travel_before_seconds ) )

      return prepared_stops


   @classmethod
   def total_occupied_seconds(
         cls,
         stops: list[ TimedLoopScheduleStop ] ) -> int:
      return sum( stop.occupied_seconds() for stop in stops )


   @classmethod
   def duration_seconds_for_stop(
         cls,
         conn: Connection,
         stop: LoopScheduleStop ) -> int | None:
      stored_block = TimeBlockBuilder.from_schedule_times(
         stop.start_time,
         stop.end_time )

      if stored_block is not None:
         return stored_block.end_seconds - stored_block.start_seconds

      return cls.default_duration_seconds_for_stop( conn, stop )


   @classmethod
   def default_duration_seconds_for_stop(
         cls,
         conn: Connection,
         stop: LoopScheduleStop ) -> int | None:
      if isinstance( stop, ItineraryAttractionRecord ):
         return ItineraryDefaultDurationProvider.fetch_attraction_default_duration_seconds(
            conn,
            stop.attraction )

      if isinstance( stop, ItineraryTransportationRecord ):
         return default_duration_seconds_for_transportation(
            conn,
            stop.transportation )

      return ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds(
         conn,
         stop.species,
         stop.exhibit,
         stop.enclosure_name )


   @classmethod
   def assign_contiguous(
         cls,
         stops: list[ TimedLoopScheduleStop ],
         *,
         start_seconds: int ) -> tuple[ list[ LoopScheduleSlot ], int ]:
      return cls.assign_contiguous_respecting_attraction_hours(
         stops,
         start_seconds=start_seconds,
         hours_by_attraction_name=None )


   @classmethod
   def assign_contiguous_respecting_attraction_hours(
         cls,
         stops: list[ TimedLoopScheduleStop ],
         *,
         start_seconds: int,
         hours_by_attraction_name: dict[ str, OperatingHours ] | None,
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
               if slot_cursor_seconds < attraction_hours.open_seconds:
                  slot_cursor_seconds = attraction_hours.open_seconds

               if (
                     slot_cursor_seconds + timed_stop.duration_seconds
                     > attraction_hours.close_seconds
               ):
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


   @classmethod
   def assign_contiguous_ending_by(
         cls,
         stops: list[ TimedLoopScheduleStop ],
         *,
         end_seconds: int ) -> tuple[ list[ LoopScheduleSlot ], int ] | None:
      start_seconds = end_seconds - cls.total_occupied_seconds( stops )

      if start_seconds < 0:
         return None

      stop_slots, segment_end_cursor_seconds = cls.assign_contiguous(
         stops,
         start_seconds=start_seconds )

      if segment_end_cursor_seconds > end_seconds:
         return None

      return stop_slots, segment_end_cursor_seconds


   @classmethod
   def save(
         cls,
         conn: Connection,
         blockers: list[ TimeBlock ],
         stop_slots: list[ LoopScheduleSlot ],
         *,
         slot_sink: LoopScheduleSlotSink | None = None ) -> bool:
      if slot_sink is None:
         slot_sink = LoopScheduleSlotSink()

      return slot_sink.save( conn, blockers, stop_slots )
