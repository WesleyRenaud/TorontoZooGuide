from __future__ import annotations

from ..animals.search.animals_matching_query import viewing_spot_key_from_values
from ..types import ScheduleTimeKey


class AnimalDiff:
   def __init__(
         self,
         species: str,
         exhibit: str,
         old_likelihood: int | None,
         new_likelihood: int | None,
         enclosure_name: str | None = None,
         is_added: bool = False,
         covered_by_talk: bool = False,
         start_time: ScheduleTimeKey = None,
         end_time: ScheduleTimeKey = None ) -> None:
      self.species = species
      self.exhibit = exhibit
      self.enclosure_name = enclosure_name
      self.old_likelihood = old_likelihood
      self.new_likelihood = new_likelihood
      self.is_added = is_added
      self.covered_by_talk = covered_by_talk
      self.start_time = start_time
      self.end_time = end_time


   def viewing_spot_key( self ) -> tuple[ str, str, str | None ]:
      return viewing_spot_key_from_values(
         self.species,
         self.exhibit,
         self.enclosure_name )


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'species': self.species,
         'exhibit': self.exhibit,
         'enclosure_name': self.enclosure_name,
         'old_likelihood': self.old_likelihood,
         'new_likelihood': self.new_likelihood,
         'is_added': self.is_added,
         'covered_by_talk': self.covered_by_talk,
         'start_time': self.start_time,
         'end_time': self.end_time,
      }
