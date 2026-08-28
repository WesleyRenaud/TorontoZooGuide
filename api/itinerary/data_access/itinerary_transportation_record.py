from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .itinerary_name_key_builder import ItineraryNameKeyBuilder
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...shared.enums import ScheduleItemKind
from ...types import ScheduleTimeKey
from ...walk_graph.domain.master_route_stop_key import AttractionMasterRouteStopKey
from ...walk_graph.domain.master_route_stop_key_builder import MasterRouteStopKeyBuilder


@dataclass( frozen=True )
class ItineraryTransportationRecord:
   transportation: str
   old_likelihood: int | None
   new_likelihood: int | None
   added_as_attraction: bool
   start_time: ScheduleTimeKey = None
   end_time: ScheduleTimeKey = None
   route: str | None = None
   bulk_transit_evaluated: bool = False
   legs: list[ ItineraryTransportationLeg ] = field( default_factory=list )
   route_marker_sequences: list[ list[ str ] ] = field( default_factory=list )


   def name_key( self ) -> str:
      return ItineraryNameKeyBuilder.build( self.transportation )


   def master_route_stop_key( self ) -> AttractionMasterRouteStopKey:
      # Reuse attraction master-route key shape so bulk packing can locate the
      # stop the same way Zoomobile did when it lived on ItineraryAttraction.
      return MasterRouteStopKeyBuilder.attraction( self.transportation )


   @property
   def attraction( self ) -> str:
      # Compatibility for call sites that read .attraction on loop stops.
      return self.transportation


   @property
   def schedule_item_kind( self ) -> ScheduleItemKind:
      return ScheduleItemKind.TRANSPORTATION
