from __future__ import annotations

from dataclasses import dataclass

from .attraction_animal_coverer import AttractionAnimalCoverer
from .attraction_animal_coverer import CoveredAnimalAttraction
from .attraction_hours_soft_pin_resolver import AttractionHoursSoftPinResolver
from .bulk_schedule_loop_pin_attacher import BulkScheduleLoopPinAttacher
from .bulk_schedule_window_prep import BulkScheduleWindowPrep
from .guardians_talk_animal_coverer import CoveredAnimalTalk
from .guardians_talk_animal_coverer import GuardiansTalkAnimalCoverer
from .loop_schedule_stop import LoopScheduleStop
from .loop_schedule_stop_extractor import LoopScheduleStopExtractor
from .loop_schedule_unit import build_loop_schedule_units
from .loop_schedule_unit import LoopScheduleUnit
from .master_route_loop_stop_grouper import MasterRouteLoopStopGrouper
from ...routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from .schedule_animals_by_master_route_loop import schedule_animals_by_master_route_loop
from ....types import Connection
from ....walk_graph.domain.viewing_spot_name_key import ViewingSpotNameKey


@dataclass( frozen=True )
class BulkScheduleLoopPackingResult:
   remaining_stops: list[ LoopScheduleStop ]
   covered_by_talk: dict[ ViewingSpotNameKey, CoveredAnimalTalk ]
   covered_by_attraction: dict[ ViewingSpotNameKey, CoveredAnimalAttraction ]
   schedule_windows: list[ ItineraryScheduleWindow ]
   loop_units: list[ LoopScheduleUnit ]


def pack_stops_into_bulk_schedule(
      conn: Connection,
      *,
      prep: BulkScheduleWindowPrep,
      stops_to_schedule: list[ LoopScheduleStop ] ) -> BulkScheduleLoopPackingResult:
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
   loop_units = build_loop_schedule_units( sorted_loop_groups )
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

   remaining_stops: list[ LoopScheduleStop ] = []

   if loop_units:
      remaining_stops, _ = schedule_animals_by_master_route_loop(
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
