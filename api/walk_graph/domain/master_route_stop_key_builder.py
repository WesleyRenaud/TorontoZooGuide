from __future__ import annotations

from .master_route_stop_key import AnimalMasterRouteStopKey
from .master_route_stop_key import AttractionMasterRouteStopKey
from ...shared.enums import ScheduleItemKind


class MasterRouteStopKeyBuilder():
   @classmethod
   def animal(
         cls,
         species: str,
         exhibit: str,
         name: str | None ) -> AnimalMasterRouteStopKey:
      return ( ScheduleItemKind.ANIMAL, species, exhibit, name )


   @classmethod
   def attraction( cls, name: str ) -> AttractionMasterRouteStopKey:
      return ( ScheduleItemKind.ATTRACTION, name )
