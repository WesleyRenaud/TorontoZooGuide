from __future__ import annotations

from ..data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from ...types import ScheduleTimeKey

WEEKDAY_TIME_FIELDS = (
   'monday_time',
   'tuesday_time',
   'wednesday_time',
   'thursday_time',
   'friday_time',
   'saturday_time',
   'sunday_time',
)


def guardians_talk_time_for_weekday(
      schedule_record: GuardiansTalkScheduleRecord,
      weekday: int ) -> ScheduleTimeKey:
   return getattr(
      schedule_record,
      WEEKDAY_TIME_FIELDS[ weekday ] )
