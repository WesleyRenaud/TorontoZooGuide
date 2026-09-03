from __future__ import annotations

from api.guardians.scheduling.guardians_talk_day_schedule_finder import GuardiansTalkDayScheduleFinder
from api.models.guardians_talk import GuardiansTalk


STATION_COORD = 0.0
TALK_TIME = '10:00 AM'


def _talk(
      *,
      name: str = 'African Lion',
      start_time: str = TALK_TIME,
      is_available: bool = True ) -> GuardiansTalk:
   return GuardiansTalk(
      name=name,
      location='Africa Savanna',
      x_coord=STATION_COORD,
      y_coord=STATION_COORD,
      start_time=start_time,
      is_available=is_available )


def Test_FindOnDaySchedule_TestInvalidStartTime_ExpectNone() -> None:
   day_schedule = [ _talk() ]

   match = GuardiansTalkDayScheduleFinder.find_on_day_schedule(
      day_schedule,
      'African Lion',
      start_time='not-a-time' )

   assert match is None


def Test_FindOnDaySchedule_TestMatchingTalk_ExpectTalk() -> None:
   day_schedule = [ _talk() ]

   match = GuardiansTalkDayScheduleFinder.find_on_day_schedule(
      day_schedule,
      'african lion',
      start_time=TALK_TIME )

   assert match is not None
   assert match.name == 'African Lion'
   assert match.start_time == TALK_TIME


def Test_FindOnDaySchedule_TestBlankTalkName_ExpectNone() -> None:
   day_schedule = [ _talk() ]

   match = GuardiansTalkDayScheduleFinder.find_on_day_schedule(
      day_schedule,
      '   ',
      start_time=TALK_TIME )

   assert match is None


def Test_FindOnDaySchedule_TestWrongStartTime_ExpectNone() -> None:
   day_schedule = [ _talk() ]

   match = GuardiansTalkDayScheduleFinder.find_on_day_schedule(
      day_schedule,
      'African Lion',
      start_time='11:00 AM' )

   assert match is None


def Test_FindOnDaySchedule_TestUnavailableTalk_ExpectUnavailableMatch() -> None:
   day_schedule = [
      _talk(
         is_available=False,
         start_time=TALK_TIME ),
   ]

   match = GuardiansTalkDayScheduleFinder.find_on_day_schedule(
      day_schedule,
      'African Lion',
      start_time=TALK_TIME )

   assert match is not None
   assert match.is_available is False
