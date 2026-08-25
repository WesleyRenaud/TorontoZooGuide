from __future__ import annotations

from dataclasses import dataclass

from .attraction_covered_animals import CoveredAnimalAttraction
from .attraction_covered_animals import merge_covered_viewing_spot_keys
from .attraction_covered_animals import viewing_spot_keys_to_cover_for_attractions
from .attraction_hours_soft_pin import attach_attraction_hours_soft_pins_to_schedule_windows
from .attraction_hours_soft_pin import resolve_attraction_hours_soft_pins
from .bulk_schedule_loop_pins import attach_loop_pins_to_schedule_windows
from .bulk_schedule_window_prep import BulkScheduleWindowPrep
from .group_stops_by_master_route_loop import group_stops_by_master_route_loop
from .guardians_talk_covered_animals import CoveredAnimalTalk
from .guardians_talk_covered_animals import filter_animals_excluding_covered
from .guardians_talk_covered_animals import viewing_spot_keys_to_cover_for_loop_pins
from .loop_schedule_stop import animals_from_stops
from .loop_schedule_stop import attractions_from_stops
from .loop_schedule_stop import LoopScheduleStop
from .loop_schedule_stop import transportations_from_stops
from .loop_schedule_unit import build_loop_schedule_units
from .loop_schedule_unit import LoopScheduleUnit
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
   animals_to_schedule = animals_from_stops( stops_to_schedule )
   attractions_to_pack = attractions_from_stops( stops_to_schedule )
   transportations_to_pack = transportations_from_stops( stops_to_schedule )
   covered_by_talk = viewing_spot_keys_to_cover_for_loop_pins(
      conn,
      prep.loop_pins,
      animals_to_schedule )
   covered_by_attraction = viewing_spot_keys_to_cover_for_attractions(
      conn,
      [
         attraction_row.attraction
         for attraction_row in attractions_to_pack
      ],
      animals_to_schedule )
   covered_keys = merge_covered_viewing_spot_keys(
      covered_by_talk,
      covered_by_attraction )
   animals_to_pack = filter_animals_excluding_covered(
      animals_to_schedule,
      covered_keys )
   stops_to_pack = [
      *animals_to_pack,
      *attractions_to_pack,
      *transportations_to_pack,
   ]
   sorted_loop_groups = group_stops_by_master_route_loop( stops_to_pack )
   loop_units = build_loop_schedule_units( sorted_loop_groups )
   schedule_windows = attach_loop_pins_to_schedule_windows(
      prep.schedule_windows,
      prep.loop_pins )

   if (
         prep.visit_date is not None
         and prep.zoo_operating_hours is not None ):
      soft_pins = resolve_attraction_hours_soft_pins(
         conn,
         attractions=[
            *attractions_to_pack,
            *transportations_to_pack,
         ],
         loop_units=loop_units,
         visit_date=prep.visit_date,
         zoo_operating_hours=prep.zoo_operating_hours )

      schedule_windows = attach_attraction_hours_soft_pins_to_schedule_windows(
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
