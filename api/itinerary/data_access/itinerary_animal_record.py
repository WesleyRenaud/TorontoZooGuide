from __future__ import annotations

from dataclasses import dataclass

from ...animals.search.species_exhibit_key import SpeciesExhibitKey
from ...animals.search.species_exhibit_key_builder import SpeciesExhibitKeyBuilder
from ...animals.search.viewing_spot_key_builder import ViewingSpotKeyBuilder
from ...types import ScheduleTimeKey
from ...walk_graph.domain.master_route_stop_key import AnimalMasterRouteStopKey
from ...walk_graph.domain.master_route_stop_key_builder import MasterRouteStopKeyBuilder


@dataclass( frozen=True )
class ItineraryAnimalRecord:
   species: str
   exhibit: str
   enclosure_name: str | None = None
   old_likelihood: int | None = None
   new_likelihood: int | None = None
   is_added: bool = False
   covered_by_talk: bool = False
   start_time: ScheduleTimeKey = None
   end_time: ScheduleTimeKey = None


   def species_exhibit_key( self ) -> SpeciesExhibitKey:
      return SpeciesExhibitKeyBuilder.from_values( self.species, self.exhibit )


   def viewing_spot_key( self ) -> tuple[ str, str, str | None ]:
      return ViewingSpotKeyBuilder.from_values(
         self.species,
         self.exhibit,
         self.enclosure_name )


   def master_route_stop_key( self ) -> AnimalMasterRouteStopKey:
      return MasterRouteStopKeyBuilder.animal(
         self.species,
         self.exhibit,
         self.enclosure_name )
