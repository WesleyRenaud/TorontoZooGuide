from __future__ import annotations

from dataclasses import dataclass

from ...animals.search.animals_matching_query import species_exhibit_key_from_values
from ...animals.search.animals_matching_query import viewing_spot_key_from_values
from ...animals.search.species_exhibit_key import SpeciesExhibitKey
from ...types import ScheduleTimeKey
from ...walk_graph.domain.master_route_stop_key import animal_master_route_stop_key
from ...walk_graph.domain.master_route_stop_key import AnimalMasterRouteStopKey


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
      return species_exhibit_key_from_values( self.species, self.exhibit )


   def viewing_spot_key( self ) -> tuple[ str, str, str | None ]:
      return viewing_spot_key_from_values(
         self.species,
         self.exhibit,
         self.enclosure_name )


   def master_route_stop_key( self ) -> AnimalMasterRouteStopKey:
      return animal_master_route_stop_key(
         self.species,
         self.exhibit,
         self.enclosure_name )
