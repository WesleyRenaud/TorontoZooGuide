from __future__ import annotations

from dataclasses import dataclass

from .master_route_stop_key import AnimalMasterRouteStopKey
from .master_route_stop_key_builder import MasterRouteStopKeyBuilder
from ...shared.enums import ScheduleItemKind
from .viewing_spot_name_key import ViewingSpotNameKey


ANIMAL_MASTER_ROUTE_STOP_KEY_LENGTH = 3


@dataclass( frozen=True )
class ViewingSpotReference:
   species: str
   exhibit: str
   name: str | None

   @property
   def kind( self ) -> ScheduleItemKind:
      return ScheduleItemKind.ANIMAL


   def key( self ) -> ViewingSpotNameKey:
      return ( self.species, self.exhibit, self.name )


   def master_route_key( self ) -> AnimalMasterRouteStopKey:
      return MasterRouteStopKeyBuilder.animal(
         self.species,
         self.exhibit,
         self.name )
