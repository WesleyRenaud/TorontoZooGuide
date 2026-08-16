from __future__ import annotations

from .itinerary_transportation_leg import ItineraryTransportationLeg
from ..types import ScheduleTimeKey


class TransportationDiff:
   def __init__(
         self,
         name: str,
         old_likelihood: int | None,
         new_likelihood: int | None,
         start_time: ScheduleTimeKey = None,
         end_time: ScheduleTimeKey = None,
         legs: list[ ItineraryTransportationLeg ] | None = None ) -> None:
      self.name = name
      self.old_likelihood = old_likelihood
      self.new_likelihood = new_likelihood
      self.start_time = start_time
      self.end_time = end_time
      self.legs = list( legs or [] )


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'old_likelihood': self.old_likelihood,
         'new_likelihood': self.new_likelihood,
         'start_time': self.start_time,
         'end_time': self.end_time,
         'legs': [ leg.to_dict() for leg in self.legs ],
      }
