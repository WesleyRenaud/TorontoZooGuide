from __future__ import annotations

from ..types import ScheduleTimeKey
from ..shared.value_conversion import ValueConversion


class WildEncounterDiff:
   def __init__(
         self,
         name: str,
         is_deleted: bool,
         start_time: ScheduleTimeKey = None,
         end_time: ScheduleTimeKey = None ) -> None:
      self.name = name
      self.is_deleted = is_deleted
      self.start_time = start_time
      self.end_time = end_time


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'is_deleted': ValueConversion.as_boolean( self.is_deleted ),
         'start_time': self.start_time,
         'end_time': self.end_time,
      }
