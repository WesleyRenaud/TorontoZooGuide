from __future__ import annotations

from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_transportation_record import ItineraryTransportationRecord
from .loop_schedule_stop import loop_schedule_stop_key
from .loop_schedule_stop import LoopScheduleStop
from ....walk_graph.master_route import default_master_route_index_by_stop_key


def sort_stops_by_master_route(
      stops: list[ LoopScheduleStop ] ) -> list[ LoopScheduleStop ]:
   if not stops:
      return []

   master_route_indexes = default_master_route_index_by_stop_key()
   mapped_stops: list[ LoopScheduleStop ] = []
   unmapped_stops: list[ LoopScheduleStop ] = []

   for stop in stops:
      if loop_schedule_stop_key( stop ) in master_route_indexes:
         mapped_stops.append( stop )
      else:
         unmapped_stops.append( stop )

   mapped_stops.sort(
      key=lambda stop: master_route_indexes[ loop_schedule_stop_key( stop ) ] )
   unmapped_stops.sort( key=_unmapped_stop_sort_key )

   return mapped_stops + unmapped_stops


def _unmapped_stop_sort_key( stop: LoopScheduleStop ) -> tuple[ str, str, str ]:
   if isinstance( stop, ( ItineraryAttractionRecord, ItineraryTransportationRecord ) ):
      return ( stop.attraction.lower(), '', '' )

   return (
      stop.exhibit.lower(),
      ( stop.enclosure_name or '' ).lower(),
      stop.species.lower(),
   )
