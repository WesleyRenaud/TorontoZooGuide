from __future__ import annotations

from ..types import Types


class AttractionDiff:
   def __init__(
         self,
         name: str,
         old_likelihood: int | None,
         new_likelihood: int | None,
         start_time: Types.ScheduleTimeKey = None,
         end_time: Types.ScheduleTimeKey = None ) -> None:
      self.name = name
      self.old_likelihood = old_likelihood
      self.new_likelihood = new_likelihood
      self.start_time = start_time
      self.end_time = end_time


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'old_likelihood': self.old_likelihood,
         'new_likelihood': self.new_likelihood,
         'start_time': self.start_time,
         'end_time': self.end_time,
      }
