from __future__ import annotations

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord
from .loop_schedule_stop import LoopScheduleStop
from .loop_schedule_stop_extractor import LoopScheduleStopExtractor
from .loop_schedule_unit import LoopScheduleUnit
from ...routing.transportation_walk_node_resolver import TransportationWalkNodeResolver
from ....walk_graph.domain.loop_side_cluster_id import LoopSideClusterId
from ....walk_graph.domain.map_location_kind import MapLocationKind
from ....walk_graph.domain.master_route_loop import MasterRouteLoop
from ....walk_graph.domain.master_route_loop_traversal_checker import MasterRouteLoopTraversalChecker
from ....walk_graph.map_location_walk_node_lookup import MapLocationWalkNodeLookup
from ....walk_graph.master_route_provider import MasterRouteProvider
from ....walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver


class LoopScheduleUnitBuilder():
   @classmethod
   def reversed(
         cls,
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


   @classmethod
   def orientations(
         cls,
         unit: LoopScheduleUnit ) -> list[ LoopScheduleUnit ]:
      if not MasterRouteLoopTraversalChecker.is_two_way( unit.traversal ):
         return [ unit ]

      return [ unit, cls.reversed( unit ) ]


   @classmethod
   def build(
         cls,
         loop_groups: list[ list[ LoopScheduleStop ] ] ) -> list[ LoopScheduleUnit ]:
      loop_ids_by_stop_key = MasterRouteProvider.loop_id_by_stop_key()
      loop_side_cluster_ids = MasterRouteProvider.loop_side_cluster_id_by_loop_id()
      loop_indexes_in_side_cluster = MasterRouteProvider.loop_index_in_side_cluster_by_loop_id()
      loops_by_id = MasterRouteProvider.loops_by_id()

      return [
         cls._from_group(
            stops,
            loop_ids_by_stop_key=loop_ids_by_stop_key,
            loop_side_cluster_ids=loop_side_cluster_ids,
            loop_indexes_in_side_cluster=loop_indexes_in_side_cluster,
            loops_by_id=loops_by_id )
         for stops in loop_groups
         if stops
      ]


   @classmethod
   def walk_node_id_for_stop(
         cls,
         stop: LoopScheduleStop ) -> str | None:
      if isinstance( stop, ItineraryTransportationRecord ):
         return TransportationWalkNodeResolver.resolve( stop.transportation )

      if isinstance( stop, ItineraryAttractionRecord ):
         walk_node = MapLocationWalkNodeLookup.for_map_location(
            MapLocationKind.ATTRACTION,
            stop.attraction )

         if walk_node is None:
            return None

         return walk_node.walk_node_id

      return ViewingSpotWalkNodeIdResolver.resolve(
         stop.species,
         stop.exhibit,
         stop.enclosure_name )


   @classmethod
   def _from_group(
         cls,
         stops: list[ LoopScheduleStop ],
         *,
         loop_ids_by_stop_key: dict,
         loop_side_cluster_ids: dict[ str, LoopSideClusterId ],
         loop_indexes_in_side_cluster: dict[ str, int ],
         loops_by_id: dict ) -> LoopScheduleUnit:
      loop_id = cls._loop_id_for_stops( stops, loop_ids_by_stop_key )

      if loop_id is None:
         return cls._unmapped( stops )

      master_route_loop = loops_by_id[ loop_id ]
      stops_in_loop_order = cls._stops_in_master_route_loop_order(
         master_route_loop,
         stops )
      entry_walk_node_id, exit_walk_node_id = (
         cls._walk_endpoint_node_ids_for_stops( stops_in_loop_order ) )

      return LoopScheduleUnit(
         loop_id=loop_id,
         stops=stops_in_loop_order,
         entry_walk_node_id=entry_walk_node_id,
         exit_walk_node_id=exit_walk_node_id,
         side_cluster_id=loop_side_cluster_ids.get( loop_id ),
         loop_index_in_side_cluster=loop_indexes_in_side_cluster.get( loop_id ),
         traversal=master_route_loop.traversal,
      )


   @classmethod
   def _walk_endpoint_node_ids_for_stops(
         cls,
         stops: list[ LoopScheduleStop ] ) -> tuple[ str | None, str | None ]:
      if not stops:
         return None, None

      return (
         cls.walk_node_id_for_stop( stops[ 0 ] ),
         cls.walk_node_id_for_stop( stops[ -1 ] ),
      )


   @classmethod
   def _stops_in_master_route_loop_order(
         cls,
         master_route_loop: MasterRouteLoop,
         stops: list[ LoopScheduleStop ] ) -> list[ LoopScheduleStop ]:
      loop_index_by_stop_key = {
         stop.master_route_key(): loop_index
         for loop_index, stop in enumerate( master_route_loop.viewing_spots )
      }
      stops_in_loop = [
         stop
         for stop in stops
         if LoopScheduleStopExtractor.stop_key( stop ) in loop_index_by_stop_key
      ]

      if not stops_in_loop:
         return list( stops )

      stops_in_loop.sort(
         key=lambda stop: loop_index_by_stop_key[ LoopScheduleStopExtractor.stop_key( stop ) ] )

      return stops_in_loop


   @classmethod
   def _loop_id_for_stops(
         cls,
         stops: list[ LoopScheduleStop ],
         loop_ids_by_stop_key: dict ) -> str | None:
      for stop in stops:
         loop_id = loop_ids_by_stop_key.get( LoopScheduleStopExtractor.stop_key( stop ) )

         if loop_id is not None:
            return loop_id

      return None


   @classmethod
   def _unmapped(
         cls,
         stops: list[ LoopScheduleStop ] ) -> LoopScheduleUnit:
      first_stop = stops[ 0 ]
      last_stop = stops[ -1 ]

      return LoopScheduleUnit(
         loop_id=None,
         stops=stops,
         entry_walk_node_id=cls.walk_node_id_for_stop( first_stop ),
         exit_walk_node_id=cls.walk_node_id_for_stop( last_stop ),
         side_cluster_id=None,
         loop_index_in_side_cluster=None,
         traversal=None,
      )
