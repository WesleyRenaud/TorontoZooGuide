from __future__ import annotations

from api.guardians.data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from api.guardians.scheduling.guardians_talk_weekday_time_resolver import GuardiansTalkWeekdayTimeResolver


STATION_COORD = 0.0
TALK_TIME = '10:00 AM'


def _schedule_record(
      *,
      monday: bool = True,
      tuesday: bool = False ) -> GuardiansTalkScheduleRecord:
   return GuardiansTalkScheduleRecord(
      name='African Lion',
      location='Africa Savanna',
      x_coord=STATION_COORD,
      y_coord=STATION_COORD,
      maximum_duration=30,
      schedule_start_date='2026-06-01',
      schedule_end_date=None,
      monday=monday,
      tuesday=tuesday,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      talk_time=TALK_TIME )


def Test_IncludesWeekday_TestScheduledMonday_ExpectTrue() -> None:
   schedule_record = _schedule_record( monday=True )

   assert GuardiansTalkWeekdayTimeResolver.includes_weekday(
      schedule_record,
      weekday=0 )


def Test_IncludesWeekday_TestUnscheduledTuesday_ExpectFalse() -> None:
   schedule_record = _schedule_record( monday=True, tuesday=False )

   assert not GuardiansTalkWeekdayTimeResolver.includes_weekday(
      schedule_record,
      weekday=1 )


def Test_TimeForWeekday_TestScheduledDay_ExpectTalkTime() -> None:
   schedule_record = _schedule_record( monday=True )

   assert GuardiansTalkWeekdayTimeResolver.time_for_weekday(
      schedule_record,
      weekday=0 ) == TALK_TIME


def Test_TimeForWeekday_TestUnscheduledDay_ExpectNone() -> None:
   schedule_record = _schedule_record( monday=True, tuesday=False )

   assert GuardiansTalkWeekdayTimeResolver.time_for_weekday(
      schedule_record,
      weekday=1 ) is None
