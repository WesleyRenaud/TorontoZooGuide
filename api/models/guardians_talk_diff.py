from __future__ import annotations

from ..shared.value_conversion import ValueConversion
from ..types import Types


class GuardiansTalkDiff:
   def __init__(
         self,
         name: str,
         is_deleted: bool,
         start_time: Types.ScheduleTimeKey = None,
         end_time: Types.ScheduleTimeKey = None,
         location: str | None = None ) -> None:
      self.name = name
      self.is_deleted = is_deleted
      self.start_time = start_time
      self.end_time = end_time
      self.location = location


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'is_deleted': ValueConversion.as_boolean( self.is_deleted ),
         'start_time': self.start_time,
         'end_time': self.end_time,
         'location': self.location,
      }
