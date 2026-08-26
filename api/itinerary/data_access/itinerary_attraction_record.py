from __future__ import annotations

from dataclasses import dataclass

from .itinerary_name_key_builder import ItineraryNameKeyBuilder
from ...types import ScheduleTimeKey
from ...walk_graph.domain.master_route_stop_key import attraction_master_route_stop_key
from ...walk_graph.domain.master_route_stop_key import AttractionMasterRouteStopKey


@dataclass( frozen=True )
class ItineraryAttractionRecord:
   attraction: str
   old_likelihood: int | None
   new_likelihood: int | None
   start_time: ScheduleTimeKey = None
   end_time: ScheduleTimeKey = None


   def name_key( self ) -> str:
      return ItineraryNameKeyBuilder.build( self.attraction )


   def master_route_stop_key( self ) -> AttractionMasterRouteStopKey:
      return attraction_master_route_stop_key( self.attraction )
