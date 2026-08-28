from __future__ import annotations

from dataclasses import dataclass

from .master_route_stop_key import AttractionMasterRouteStopKey
from .master_route_stop_key_builder import MasterRouteStopKeyBuilder
from ...shared.enums import ScheduleItemKind


ATTRACTION_MASTER_ROUTE_STOP_KEY_LENGTH = 1


@dataclass( frozen=True )
class AttractionRouteStop:
   name: str

   @property
   def kind( self ) -> ScheduleItemKind:
      return ScheduleItemKind.ATTRACTION


   def master_route_key( self ) -> AttractionMasterRouteStopKey:
      return MasterRouteStopKeyBuilder.attraction( self.name )
