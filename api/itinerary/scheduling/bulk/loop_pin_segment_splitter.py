from __future__ import annotations

from .loop_pin_gap_step import LoopPinGapStep
from .loop_pin_schedule_step import LoopPinScheduleStep
from .loop_pin_stop_segment import LoopPinStopSegment
from .loop_schedule_stop import LoopScheduleStop
from .loop_schedule_stop_extractor import LoopScheduleStopExtractor
from ...routing.loop_schedule_pin import LoopSchedulePin
from ....walk_graph.master_route_provider import MasterRouteProvider


class LoopPinSegmentSplitter():
   @classmethod
   def schedule_steps(
         cls,
         stops: list[ LoopScheduleStop.Stop ],
         *,
         loop_id: str,
         loop_pins: list[ LoopSchedulePin ],
         window_end_seconds: int,
      ) -> list[ LoopPinScheduleStep.Step ]:
      stop_segments = cls.split_stops(
         stops,
         loop_id=loop_id,
         loop_pins=loop_pins )
      steps: list[ LoopPinScheduleStep.Step ] = []

      for pin_index, loop_pin in enumerate( loop_pins ):
         before_pin_stops = stop_segments[ pin_index ]

         if before_pin_stops:
            steps.append(
               LoopPinStopSegment(
                  stops=before_pin_stops,
                  end_before_seconds=loop_pin.start_seconds,
                  anchor_at_end=True,
               ) )

         steps.append( LoopPinGapStep( loop_pin=loop_pin ) )

      after_last_pin_stops = stop_segments[ len( loop_pins ) ]

      if after_last_pin_stops:
         steps.append(
            LoopPinStopSegment(
               stops=after_last_pin_stops,
               end_before_seconds=window_end_seconds,
               anchor_at_end=False,
            ) )

      return steps


   @classmethod
   def split_stops(
         cls,
         stops: list[ LoopScheduleStop.Stop ],
         *,
         loop_id: str,
         loop_pins: list[ LoopSchedulePin ],
      ) -> list[ list[ LoopScheduleStop.Stop ] ]:
      pin_boundaries = [
         loop_pin.viewing_spot_index
         for loop_pin in loop_pins
      ]
      segments: list[ list[ LoopScheduleStop.Stop ] ] = [
         [] for _ in range( len( loop_pins ) + 1 )
      ]

      for stop in stops:
         viewing_spot_index = cls.viewing_spot_index_for_stop(
            loop_id,
            stop )
         segment_index = cls.segment_index_for_viewing_spot(
            viewing_spot_index,
            pin_boundaries=pin_boundaries )
         segments[ segment_index ].append( stop )

      return segments


   @classmethod
   def segment_index_for_viewing_spot(
         cls,
         viewing_spot_index: int | None,
         *,
         pin_boundaries: list[ int ],
      ) -> int:
      if viewing_spot_index is None:
         return len( pin_boundaries )

      for pin_index, pin_boundary in enumerate( pin_boundaries ):
         if viewing_spot_index <= pin_boundary:
            return pin_index

      return len( pin_boundaries )


   @classmethod
   def animals_before_first_pin(
         cls,
         stops: list[ LoopScheduleStop.Stop ],
         *,
         loop_id: str,
         loop_pins: list[ LoopSchedulePin ],
      ) -> list[ LoopScheduleStop.Stop ]:
      segments = cls.split_stops(
         stops,
         loop_id=loop_id,
         loop_pins=loop_pins )

      if not segments:
         return []

      return segments[ 0 ]


   @classmethod
   def viewing_spot_index_for_stop(
         cls,
         loop_id: str,
         stop: LoopScheduleStop.Stop ) -> int | None:
      master_route_loop = MasterRouteProvider.loops_by_id().get( loop_id )

      if master_route_loop is None:
         return None

      stop_key = LoopScheduleStopExtractor.stop_key( stop )
      matching_indexes = [
         index
         for index, route_stop in enumerate( master_route_loop.viewing_spots )
         if route_stop.master_route_key() == stop_key
      ]

      if not matching_indexes:
         return None

      return min( matching_indexes )
