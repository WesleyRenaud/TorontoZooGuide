from __future__ import annotations

from ..shared.value_conversion import ValueConversion
from ..types import Coordinate, ScheduleTimeKey


class WildEncounter:
   def __init__(
         self,
         name: str,
         meeting_spot: str,
         link: str,
         start_time: ScheduleTimeKey = None,
         maximum_duration: int | None = None,
         end_time: ScheduleTimeKey = None,
         x_coord: float | None = None,
         y_coord: float | None = None,
         is_available: bool = True,
         unavailable_message: str | None = None,
         is_deleted: bool = False ) -> None:
      self.name = name
      self.meeting_spot = meeting_spot
      self.link = link
      self.start_time = start_time
      self.maximum_duration = maximum_duration
      self.end_time = end_time
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.is_available = is_available
      self.unavailable_message = unavailable_message
      self.is_deleted = is_deleted


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'meeting_spot': self.meeting_spot,
         'link': self.link,
         'start_time': self.start_time,
         'maximum_duration': self.maximum_duration,
         'end_time': self.end_time,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'is_available': ValueConversion.as_boolean( self.is_available ),
         'unavailable_message': self.unavailable_message,
         'is_deleted': ValueConversion.as_boolean( self.is_deleted )
      }
