from __future__ import annotations

from ..types import ScheduleTimeKey


class AnimalDiff:
   def __init__(
         self,
         species: str,
         exhibit: str,
         old_likelihood: int | None,
         new_likelihood: int | None,
         is_added: bool = False,
         start_time: ScheduleTimeKey = None,
         end_time: ScheduleTimeKey = None ) -> None:
      self.species = species
      self.exhibit = exhibit
      self.old_likelihood = old_likelihood
      self.new_likelihood = new_likelihood
      self.is_added = is_added
      self.start_time = start_time
      self.end_time = end_time


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'species': self.species,
         'exhibit': self.exhibit,
         'old_likelihood': self.old_likelihood,
         'new_likelihood': self.new_likelihood,
         'is_added': self.is_added,
         'start_time': self.start_time,
         'end_time': self.end_time,
      }
