from __future__ import annotations

from .itinerary_transportation_leg import ItineraryTransportationLeg
from .itinerary_transportation_station import ItineraryTransportationStation
from ..shared.value_conversion import ValueConversion
from ..types import ScheduleTimeKey


class ItineraryTransportation:
   def __init__(
         self,
         name: str,
         *,
         old_likelihood: int | None = None,
         likelihood: int | None = None,
         start_time: ScheduleTimeKey = None,
         end_time: ScheduleTimeKey = None,
         x_coord: float | None = None,
         y_coord: float | None = None,
         main_station: str | None = None,
         legs: list[ ItineraryTransportationLeg ] | None = None,
         stations: list[ ItineraryTransportationStation ] | None = None,
         added_as_attraction: bool = False,
         route_duration_minutes: int | None = None ) -> None:
      self.name = name
      self.old_likelihood = old_likelihood
      self.likelihood = likelihood
      self.start_time = start_time
      self.end_time = end_time
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.main_station = main_station
      self.legs = legs or []
      self.stations = stations or []
      self.added_as_attraction = added_as_attraction
      self.route_duration_minutes = route_duration_minutes


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'old_likelihood': self.old_likelihood,
         'likelihood': self.likelihood,
         'start_time': self.start_time,
         'end_time': self.end_time,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'main_station': self.main_station,
         'legs': [ leg.to_dict() for leg in self.legs ],
         'stations': [ station.to_dict() for station in self.stations ],
         'added_as_attraction': ValueConversion.as_boolean(
            self.added_as_attraction ),
         'route_duration_minutes': self.route_duration_minutes,
      }
