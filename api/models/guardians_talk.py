from __future__ import annotations

from ..types import Coordinate, ScheduleTimeKey
from ..zoo_util import ZooUtil


class GuardiansTalk:
   def __init__(
         self,
         name: str,
         location: str,
         x_coord: Coordinate,
         y_coord: Coordinate,
         start_time: ScheduleTimeKey = None,
         maximum_duration: int | None = None,
         end_time: ScheduleTimeKey = None,
         is_available: bool = True,
         unavailable_message: str | None = None,
         is_deleted: bool = False ) -> None:
      self.name = name
      self.location = location
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.start_time = start_time
      self.maximum_duration = maximum_duration
      self.end_time = end_time
      self.is_available = is_available
      self.unavailable_message = unavailable_message
      self.is_deleted = is_deleted


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'location': self.location,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'start_time': self.start_time,
         'maximum_duration': self.maximum_duration,
         'end_time': self.end_time,
         'is_available': ZooUtil.as_boolean( self.is_available ),
         'unavailable_message': self.unavailable_message,
         'is_deleted': ZooUtil.as_boolean( self.is_deleted )
      }
