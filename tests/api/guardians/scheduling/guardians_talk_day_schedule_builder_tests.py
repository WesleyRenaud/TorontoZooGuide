from __future__ import annotations

from api.guardians.data_access.guardians_talk_day_schedule_record import GuardiansTalkDayScheduleRecord
from api.guardians.scheduling.guardians_talk_day_schedule_builder import GuardiansTalkDayScheduleBuilder
from api.shared.enums.position import Position


STATION_COORD = 0.0
TALK_TIME = '10:00 AM'
MAXIMUM_DURATION = 30


def _day_schedule_record( *, talk_time: str ) -> GuardiansTalkDayScheduleRecord:
   return GuardiansTalkDayScheduleRecord(
      name='African Lion',
      location='Africa Savanna',
      x_coord=STATION_COORD,
      y_coord=STATION_COORD,
      maximum_duration=MAXIMUM_DURATION,
      talk_time=talk_time )


def Test_BuildFromRecords_TestDayScheduleRecord_ExpectAvailableTalkWithEndTime() -> None:
   records = [ _day_schedule_record( talk_time=TALK_TIME ) ]

   talks = GuardiansTalkDayScheduleBuilder.build_from_records( records )

   assert len( talks ) == 1
   assert talks[ Position.FIRST ].name == 'African Lion'
   assert talks[ Position.FIRST ].location == 'Africa Savanna'
   assert talks[ Position.FIRST ].start_time == TALK_TIME
   assert talks[ Position.FIRST ].end_time == '10:30 AM'
   assert talks[ Position.FIRST ].is_available is True
   assert talks[ Position.FIRST ].unavailable_message is None


def Test_BuildFromRecords_TestMultipleTimesOnSameDay_ExpectBothTalksWithEndTimes() -> None:
   records = [
      _day_schedule_record( talk_time='2:00 PM' ),
      _day_schedule_record( talk_time='3:30 PM' ),
   ]

   talks = GuardiansTalkDayScheduleBuilder.build_from_records( records )

   assert sorted( talk.start_time for talk in talks ) == [ '2:00 PM', '3:30 PM' ]
   assert all( talk.end_time is not None for talk in talks )
   assert all( talk.is_available is True for talk in talks )
