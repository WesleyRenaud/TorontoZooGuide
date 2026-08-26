from __future__ import annotations

from ..data_access.guardians_talk_day_schedule_record import GuardiansTalkDayScheduleRecord
from ...models import GuardiansTalk
from ...shared.calendar_dates import DateValues


class GuardiansTalkDayScheduleBuilder():
   @classmethod
   def build_from_records(
         cls,
         records: list[ GuardiansTalkDayScheduleRecord ] ) -> list[ GuardiansTalk ]:
      return [
         GuardiansTalk(
            name=record.name,
            location=record.location,
            x_coord=record.x_coord,
            y_coord=record.y_coord,
            start_time=record.talk_time,
            maximum_duration=record.maximum_duration,
            end_time=DateValues.add_minutes_to_time(
               record.talk_time,
               record.maximum_duration ),
            is_available=True,
            unavailable_message=None )
         for record in records
      ]
