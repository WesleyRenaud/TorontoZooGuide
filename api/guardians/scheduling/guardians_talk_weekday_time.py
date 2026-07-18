from __future__ import annotations

from ..data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from ...shared.calendar_dates import CalendarDates
from ...types import ScheduleTimeKey

WEEKDAY_FLAG_FIELDS = (
   'monday',
   'tuesday',
   'wednesday',
   'thursday',
   'friday',
   'saturday',
   'sunday',
)


def guardians_talk_weekday_flags(
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


def guardians_talk_includes_weekday(
      schedule_record: GuardiansTalkScheduleRecord,
      weekday: int ) -> bool:
   return CalendarDates.schedule_includes_weekday(
      weekday,
      guardians_talk_weekday_flags( schedule_record ) )


def guardians_talk_time_for_weekday(
      schedule_record: GuardiansTalkScheduleRecord,
      weekday: int ) -> ScheduleTimeKey:
   if not guardians_talk_includes_weekday( schedule_record, weekday ):
      return None

   return schedule_record.talk_time
