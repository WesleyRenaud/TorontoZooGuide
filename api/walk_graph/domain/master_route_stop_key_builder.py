from __future__ import annotations

from .animal_master_route_stop_key import AnimalMasterRouteStopKey
from .attraction_master_route_stop_key import AttractionMasterRouteStopKey
from ...shared.enums import ScheduleItemKind


class MasterRouteStopKeyBuilder():
   @classmethod
   def animal(
         cls,
         species: str,
         exhibit: str,
         name: str | None ) -> AnimalMasterRouteStopKey.Key:
      return ( ScheduleItemKind.ANIMAL, species, exhibit, name )


   @classmethod
   def attraction( cls, name: str ) -> AttractionMasterRouteStopKey.Key:
      return ( ScheduleItemKind.ATTRACTION, name )
