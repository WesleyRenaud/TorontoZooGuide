from __future__ import annotations

from ..domain.guardians_talk_name_filter import GuardiansTalkNameFilter
from ...models import GuardiansTalk
from ...shared.calendar_dates import DateValues
from ...types import Types


class GuardiansTalkDayScheduleFinder():
   @classmethod
   def find_on_day_schedule(
         cls,
         day_schedule: list[ GuardiansTalk ],
         talk_name: str,
         *,
         start_time: Types.ScheduleTimeKey ) -> GuardiansTalk | None:
      talk_filter = GuardiansTalkNameFilter( name=talk_name )

      if talk_filter.should_return_empty():
         return None

      normalized_start_time = DateValues.normalize_schedule_time(
         start_time )

      if normalized_start_time is None:
         return None

      for row in day_schedule:
         if not talk_filter.allows_talk_name( row.name ):
            continue

         row_start_time = DateValues.normalize_schedule_time(
            row.start_time )

         if row_start_time == normalized_start_time:
            return row

      return None
