from __future__ import annotations

from ..data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from ...shared.calendar_dates import CalendarDates
from ...types import ScheduleTimeKey


class GuardiansTalkWeekdayTimeResolver():
   @classmethod
   def weekday_flags(
         cls,
         schedule_record: GuardiansTalkScheduleRecord ) -> list[ bool ]:
      return [
         schedule_record.monday,
         schedule_record.tuesday,
         schedule_record.wednesday,
         schedule_record.thursday,
         schedule_record.friday,
         schedule_record.saturday,
         schedule_record.sunday,
      ]


   @classmethod
   def includes_weekday(
         cls,
         schedule_record: GuardiansTalkScheduleRecord,
         weekday: int ) -> bool:
      return CalendarDates.schedule_includes_weekday(
         weekday,
         cls.weekday_flags( schedule_record ) )


   @classmethod
   def time_for_weekday(
         cls,
         schedule_record: GuardiansTalkScheduleRecord,
         weekday: int ) -> ScheduleTimeKey:
      if not cls.includes_weekday( schedule_record, weekday ):
         return None

      return schedule_record.talk_time
