from __future__ import annotations

from .itinerary_transportation_leg import ItineraryTransportationLeg
from ..types import Types


class TransportationDiff:
   def __init__(
         self,
         name: str,
         old_likelihood: int | None,
         new_likelihood: int | None,
         start_time: Types.ScheduleTimeKey = None,
         end_time: Types.ScheduleTimeKey = None,
         legs: list[ ItineraryTransportationLeg ] | None = None,
         *,
         route: str | None = None,
         route_marker_sequences: list[ list[ str ] ] | None = None,
         added_as_attraction: bool,
         bulk_transit_evaluated: bool = False ) -> None:
      self.name = name
      self.old_likelihood = old_likelihood
      self.new_likelihood = new_likelihood
      self.start_time = start_time
      self.end_time = end_time
      self.legs = list( legs or [] )
      self.route = route
      self.route_marker_sequences = list( route_marker_sequences or [] )
      self.added_as_attraction = added_as_attraction
      self.bulk_transit_evaluated = bulk_transit_evaluated


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'old_likelihood': self.old_likelihood,
         'new_likelihood': self.new_likelihood,
         'start_time': self.start_time,
         'end_time': self.end_time,
         'legs': [ leg.to_dict() for leg in self.legs ],
         'route': self.route,
         'route_marker_sequences': self.route_marker_sequences,
         'added_as_attraction': self.added_as_attraction,
         'bulk_transit_evaluated': self.bulk_transit_evaluated,
      }
