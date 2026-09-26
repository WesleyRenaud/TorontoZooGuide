from __future__ import annotations

from api.guardians.data_access.guardians_talk_day_schedule_record import GuardiansTalkDayScheduleRecord
from api.guardians.scheduling.guardians_talk_day_schedule_builder import GuardiansTalkDayScheduleBuilder
from api.shared.calendar_dates import DateValues
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
   record = _day_schedule_record( talk_time=TALK_TIME )
   records = [ record ]

   talks = GuardiansTalkDayScheduleBuilder.build_from_records( records )

   talk = talks[ Position.FIRST ]
   assert len( talks ) == 1
   assert talk.name == record.name
   assert talk.location == record.location
   assert talk.start_time == record.talk_time
   assert talk.end_time == DateValues.add_minutes_to_time(
      record.talk_time,
      record.maximum_duration )
   assert talk.is_available is True
   assert talk.unavailable_message is None


def Test_BuildFromRecords_TestMultipleTimesOnSameDay_ExpectBothTalksWithEndTimes() -> None:
   afternoon = _day_schedule_record( talk_time='2:00 PM' )
   later = _day_schedule_record( talk_time='3:30 PM' )
   records = [ afternoon, later ]

   talks = GuardiansTalkDayScheduleBuilder.build_from_records( records )

   assert sorted( talk.start_time for talk in talks ) == [
      afternoon.talk_time,
      later.talk_time,
   ]
   assert all( talk.end_time is not None for talk in talks )
   assert all( talk.is_available is True for talk in talks )
