from __future__ import annotations

from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord
from .loop_schedule_stop import LoopScheduleStop
from .loop_schedule_stop_extractor import LoopScheduleStopExtractor
from ....walk_graph.master_route_provider import MasterRouteProvider


class MasterRouteStopSorter():
   @classmethod
   def sort(
         cls,
         stops: list[ LoopScheduleStop.Stop ] ) -> list[ LoopScheduleStop.Stop ]:
      if not stops:
         return []

      master_route_indexes = MasterRouteProvider.route_index_by_stop_key()
      mapped_stops: list[ LoopScheduleStop.Stop ] = []
      unmapped_stops: list[ LoopScheduleStop.Stop ] = []

      for stop in stops:
         if LoopScheduleStopExtractor.stop_key( stop ) in master_route_indexes:
            mapped_stops.append( stop )
         else:
            unmapped_stops.append( stop )

      mapped_stops.sort(
         key=lambda stop: master_route_indexes[
            LoopScheduleStopExtractor.stop_key( stop ) ] )
      unmapped_stops.sort( key=cls._unmapped_stop_sort_key )

      return mapped_stops + unmapped_stops


   @classmethod
   def _unmapped_stop_sort_key(
         cls,
         stop: LoopScheduleStop.Stop ) -> tuple[ str, str, str ]:
      if isinstance( stop, ( ItineraryAttractionRecord, ItineraryTransportationRecord ) ):
         return ( stop.attraction.lower(), '', '' )

      return (
         stop.exhibit.lower(),
         ( stop.enclosure_name or '' ).lower(),
         stop.species.lower(),
      )
