from __future__ import annotations

from dataclasses import dataclass

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord
from .loop_schedule_stop import loop_schedule_stop_key
from .loop_schedule_stop import LoopScheduleStop
from ....walk_graph.domain.loop_side_cluster_id import LoopSideClusterId
from ....walk_graph.domain.map_location_kind import MapLocationKind
from ....walk_graph.domain.master_route_loop import is_two_way_loop_traversal
from ....walk_graph.domain.master_route_loop import MasterRouteLoop
from ....walk_graph.map_location_walk_node_lookup import walk_node_for_map_location
from ....walk_graph.master_route import default_loop_id_by_stop_key
from ....walk_graph.master_route import default_loop_index_in_side_cluster_by_loop_id
from ....walk_graph.master_route import default_loop_side_cluster_id_by_loop_id
from ....walk_graph.master_route import default_master_route_loop_by_id
from ....walk_graph.walk_node_id_for_viewing_spot import walk_node_id_for_viewing_spot


@dataclass( frozen=True )
class LoopScheduleUnit:
   loop_id: str | None
   stops: list[ LoopScheduleStop ]
   entry_walk_node_id: str | None
   exit_walk_node_id: str | None
   side_cluster_id: str | None
   loop_index_in_side_cluster: int | None
   traversal: str | None


def loop_schedule_unit_reversed(
      unit: LoopScheduleUnit ) -> LoopScheduleUnit:
   return LoopScheduleUnit(
      loop_id=unit.loop_id,
      stops=list( reversed( unit.stops ) ),
      entry_walk_node_id=unit.exit_walk_node_id,
      exit_walk_node_id=unit.entry_walk_node_id,
      side_cluster_id=unit.side_cluster_id,
      loop_index_in_side_cluster=unit.loop_index_in_side_cluster,
      traversal=unit.traversal,
   )


def loop_schedule_unit_orientations(
      unit: LoopScheduleUnit ) -> list[ LoopScheduleUnit ]:
   if not is_two_way_loop_traversal( unit.traversal ):
      return [ unit ]

   return [ unit, loop_schedule_unit_reversed( unit ) ]


def build_loop_schedule_units(
      loop_groups: list[ list[ LoopScheduleStop ] ] ) -> list[ LoopScheduleUnit ]:
   loop_ids_by_stop_key = default_loop_id_by_stop_key()
   loop_side_cluster_ids = default_loop_side_cluster_id_by_loop_id()
   loop_indexes_in_side_cluster = default_loop_index_in_side_cluster_by_loop_id()
   loops_by_id = default_master_route_loop_by_id()

   return [
      _loop_schedule_unit_from_group(
         stops,
         loop_ids_by_stop_key=loop_ids_by_stop_key,
         loop_side_cluster_ids=loop_side_cluster_ids,
         loop_indexes_in_side_cluster=loop_indexes_in_side_cluster,
         loops_by_id=loops_by_id )
      for stops in loop_groups
      if stops
   ]


def _loop_schedule_unit_from_group(
      stops: list[ LoopScheduleStop ],
      *,
      loop_ids_by_stop_key: dict,
      loop_side_cluster_ids: dict[ str, LoopSideClusterId ],
      loop_indexes_in_side_cluster: dict[ str, int ],
      loops_by_id: dict ) -> LoopScheduleUnit:
   loop_id = _loop_id_for_stops( stops, loop_ids_by_stop_key )

   if loop_id is None:
      return _unmapped_loop_schedule_unit( stops )

   master_route_loop = loops_by_id[ loop_id ]
   stops_in_loop_order = _stops_in_master_route_loop_order(
      master_route_loop,
      stops )
   entry_walk_node_id, exit_walk_node_id = (
      _loop_walk_endpoint_node_ids_for_stops( stops_in_loop_order ) )

   return LoopScheduleUnit(
      loop_id=loop_id,
      stops=stops_in_loop_order,
      entry_walk_node_id=entry_walk_node_id,
      exit_walk_node_id=exit_walk_node_id,
      side_cluster_id=loop_side_cluster_ids.get( loop_id ),
      loop_index_in_side_cluster=loop_indexes_in_side_cluster.get( loop_id ),
      traversal=master_route_loop.traversal,
   )


def _loop_walk_endpoint_node_ids_for_stops(
      stops: list[ LoopScheduleStop ] ) -> tuple[ str | None, str | None ]:
   if not stops:
      return None, None

   return (
      walk_node_id_for_loop_schedule_stop( stops[ 0 ] ),
      walk_node_id_for_loop_schedule_stop( stops[ -1 ] ),
   )


def _stops_in_master_route_loop_order(
      master_route_loop: MasterRouteLoop,
      stops: list[ LoopScheduleStop ] ) -> list[ LoopScheduleStop ]:
   loop_index_by_stop_key = {
      stop.master_route_key(): loop_index
      for loop_index, stop in enumerate( master_route_loop.viewing_spots )
   }
   stops_in_loop = [
      stop
      for stop in stops
      if loop_schedule_stop_key( stop ) in loop_index_by_stop_key
   ]

   if not stops_in_loop:
      return list( stops )

   stops_in_loop.sort(
      key=lambda stop: loop_index_by_stop_key[ loop_schedule_stop_key( stop ) ] )

   return stops_in_loop


def walk_node_id_for_loop_schedule_stop(
      stop: LoopScheduleStop ) -> str | None:
   if isinstance( stop, ( ItineraryAttractionRecord, ItineraryTransportationRecord ) ):
      walk_node = walk_node_for_map_location(
         MapLocationKind.ATTRACTION,
         stop.attraction )

      if walk_node is None:
         return None

      return walk_node.walk_node_id

   return walk_node_id_for_viewing_spot(
      stop.species,
      stop.exhibit,
      stop.enclosure_name )


def _loop_id_for_stops(
      stops: list[ LoopScheduleStop ],
      loop_ids_by_stop_key: dict ) -> str | None:
   for stop in stops:
      loop_id = loop_ids_by_stop_key.get( loop_schedule_stop_key( stop ) )

      if loop_id is not None:
         return loop_id

   return None


def _unmapped_loop_schedule_unit(
      stops: list[ LoopScheduleStop ] ) -> LoopScheduleUnit:
   first_stop = stops[ 0 ]
   last_stop = stops[ -1 ]

   return LoopScheduleUnit(
      loop_id=None,
      stops=stops,
      entry_walk_node_id=walk_node_id_for_loop_schedule_stop( first_stop ),
      exit_walk_node_id=walk_node_id_for_loop_schedule_stop( last_stop ),
      side_cluster_id=None,
      loop_index_in_side_cluster=None,
      traversal=None,
   )
