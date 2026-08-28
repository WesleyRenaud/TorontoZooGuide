from __future__ import annotations

from .attraction_animal_coverer import AttractionAnimalCoverer
from .attraction_hours_soft_pin_resolver import AttractionHoursSoftPinResolver
from .bulk_schedule_loop_packing_result import BulkScheduleLoopPackingResult
from .bulk_schedule_loop_pin_attacher import BulkScheduleLoopPinAttacher
from .bulk_schedule_window_prep import BulkScheduleWindowPrep
from .guardians_talk_animal_coverer import GuardiansTalkAnimalCoverer
from .loop_schedule_stop import LoopScheduleStop
from .loop_schedule_stop_extractor import LoopScheduleStopExtractor
from .loop_schedule_unit_builder import LoopScheduleUnitBuilder
from .master_route_loop_scheduler import MasterRouteLoopScheduler
from .master_route_loop_stop_grouper import MasterRouteLoopStopGrouper
from ....types import Types


class BulkScheduleLoopPacker():
   @classmethod
   def pack_stops(
         cls,
         conn: Types.Connection,
         *,
         prep: BulkScheduleWindowPrep,
         stops_to_schedule: list[ LoopScheduleStop.Stop ] ) -> BulkScheduleLoopPackingResult:
      animals_to_schedule = LoopScheduleStopExtractor.animals_from( stops_to_schedule )
      attractions_to_pack = LoopScheduleStopExtractor.attractions_from( stops_to_schedule )
      transportations_to_pack = LoopScheduleStopExtractor.transportations_from( stops_to_schedule )
      covered_by_talk = GuardiansTalkAnimalCoverer.keys_to_cover(
         conn,
         prep.loop_pins,
         animals_to_schedule )
      covered_by_attraction = AttractionAnimalCoverer.keys_to_cover(
         conn,
         [
            attraction_row.attraction
            for attraction_row in attractions_to_pack
         ],
         animals_to_schedule )
      covered_keys = AttractionAnimalCoverer.merge_keys(
         covered_by_talk,
         covered_by_attraction )
      animals_to_pack = GuardiansTalkAnimalCoverer.excluding_covered(
         animals_to_schedule,
         covered_keys )
      stops_to_pack = [
         *animals_to_pack,
         *attractions_to_pack,
         *transportations_to_pack,
      ]
      sorted_loop_groups = MasterRouteLoopStopGrouper.group( stops_to_pack )
      loop_units = LoopScheduleUnitBuilder.build( sorted_loop_groups )
      schedule_windows = BulkScheduleLoopPinAttacher.attach_to_windows(
         prep.schedule_windows,
         prep.loop_pins )

      if (
            prep.visit_date is not None
            and prep.zoo_operating_hours is not None ):
         soft_pins = AttractionHoursSoftPinResolver.resolve(
            conn,
            attractions=[
               *attractions_to_pack,
               *transportations_to_pack,
            ],
            loop_units=loop_units,
            visit_date=prep.visit_date,
            zoo_operating_hours=prep.zoo_operating_hours )

         schedule_windows = AttractionHoursSoftPinResolver.attach_to_windows(
            schedule_windows,
            soft_pins )

      remaining_stops: list[ LoopScheduleStop.Stop ] = []

      if loop_units:
         remaining_stops, _ = MasterRouteLoopScheduler.schedule(
            conn,
            loop_units,
            blockers=prep.blockers,
            schedule_windows=schedule_windows,
            schedule_cursor_seconds=prep.start_state.schedule_anchor_seconds,
            walk_graph=prep.walk_graph,
            start_node_id=prep.start_state.start_node_id )

      return BulkScheduleLoopPackingResult(
         remaining_stops=remaining_stops,
         covered_by_talk=covered_by_talk,
         covered_by_attraction=covered_by_attraction,
         schedule_windows=schedule_windows,
         loop_units=loop_units )
