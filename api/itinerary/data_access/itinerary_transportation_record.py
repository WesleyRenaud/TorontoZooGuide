from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .itinerary_name_key import itinerary_name_key
from .itinerary_transportation_leg_record import ItineraryTransportationLegRecord
from ...shared.enums import ScheduleItemKind
from ...types import ScheduleTimeKey
from ...walk_graph.domain.master_route_stop_key import attraction_master_route_stop_key
from ...walk_graph.domain.master_route_stop_key import AttractionMasterRouteStopKey


@dataclass( frozen=True )
class ItineraryTransportationRecord:
   transportation: str
   old_likelihood: int | None
   new_likelihood: int | None
   start_time: ScheduleTimeKey = None
   end_time: ScheduleTimeKey = None
   added_as_attraction: bool = False
   legs: list[ ItineraryTransportationLegRecord ] = field( default_factory=list )


   def name_key( self ) -> str:
      return itinerary_name_key( self.transportation )


   def master_route_stop_key( self ) -> AttractionMasterRouteStopKey:
      # Reuse attraction master-route key shape so bulk packing can locate the
      # stop the same way Zoomobile did when it lived on ItineraryAttraction.
      return attraction_master_route_stop_key( self.transportation )


   @property
   def attraction( self ) -> str:
      # Compatibility for call sites that read .attraction on loop stops.
      return self.transportation


   @property
   def schedule_item_kind( self ) -> ScheduleItemKind:
      return ScheduleItemKind.TRANSPORTATION
