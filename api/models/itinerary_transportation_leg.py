from __future__ import annotations

from ..types import ScheduleTimeKey


class ItineraryTransportationLeg:
   def __init__(
         self,
         from_station: str,
         to_station: str,
         start_time: ScheduleTimeKey,
         end_time: ScheduleTimeKey,
         transportation: str,
         added_as_attraction: bool ) -> None:
      self.from_station = from_station
      self.to_station = to_station
      self.start_time = start_time
      self.end_time = end_time
      self.transportation = transportation
      self.added_as_attraction = added_as_attraction


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'from_station': self.from_station,
         'to_station': self.to_station,
         'start_time': self.start_time,
         'end_time': self.end_time,
      }
