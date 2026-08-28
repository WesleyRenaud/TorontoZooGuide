from __future__ import annotations

from ..shared.value_conversion import ValueConversion
from ..types import Types


class WildEncounterDiff:
   def __init__(
         self,
         name: str,
         is_deleted: bool,
         start_time: Types.ScheduleTimeKey = None,
         end_time: Types.ScheduleTimeKey = None,
         meeting_spot: str | None = None,
         link: str | None = None ) -> None:
      self.name = name
      self.is_deleted = is_deleted
      self.start_time = start_time
      self.end_time = end_time
      self.meeting_spot = meeting_spot
      self.link = link


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'is_deleted': ValueConversion.as_boolean( self.is_deleted ),
         'start_time': self.start_time,
         'end_time': self.end_time,
         'meeting_spot': self.meeting_spot,
         'link': self.link,
      }
