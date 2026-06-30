from __future__ import annotations

from dataclasses import dataclass

from ...animals.search.animals_matching_query import species_exhibit_key_from_values
from ...animals.search.animals_matching_query import viewing_spot_key_from_values
from ...types import ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryAnimalRecord:
   species: str
   exhibit: str
   enclosure_name: str | None = None
   old_likelihood: int | None = None
   new_likelihood: int | None = None
   is_added: bool = False
   start_time: ScheduleTimeKey = None
   end_time: ScheduleTimeKey = None


   def species_exhibit_key( self ) -> tuple[ str, str ]:
      return species_exhibit_key_from_values( self.species, self.exhibit )


   def viewing_spot_key( self ) -> tuple[ str, str, str | None ]:
      return viewing_spot_key_from_values(
         self.species,
         self.exhibit,
         self.enclosure_name )
