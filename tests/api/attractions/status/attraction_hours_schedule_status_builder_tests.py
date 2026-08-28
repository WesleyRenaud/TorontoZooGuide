from __future__ import annotations

from api.attractions.status.attraction_hours_schedule_status_builder import AttractionHoursScheduleStatusBuilder


ATTRACTION_NAME = 'Conservation Carousel'
SCHEDULE_START_DATE = '2026-06-01'
SCHEDULE_END_DATE = '2026-06-30'
WEEKDAY_START_TIME = '10:00 AM'
WEEKDAY_END_TIME = '4:00 PM'
WEEKEND_START_TIME = '11:00 AM'
WEEKEND_END_TIME = '5:00 PM'


def Test_BuildHoursSchedule_TestExplicitDates_ExpectScheduleFieldsRetained() -> None:
   schedule = AttractionHoursScheduleStatusBuilder.build_hours_schedule(
      attraction=ATTRACTION_NAME,
      start_date=SCHEDULE_START_DATE,
      end_date=SCHEDULE_END_DATE,
      weekday_start_time=WEEKDAY_START_TIME,
      weekday_end_time=WEEKDAY_END_TIME,
      weekend_holiday_start_time=WEEKEND_START_TIME,
      weekend_holiday_end_time=WEEKEND_END_TIME )

   assert schedule.attraction == ATTRACTION_NAME
   assert schedule.start_date == SCHEDULE_START_DATE
   assert schedule.end_date == SCHEDULE_END_DATE
   assert schedule.weekday_start_time == WEEKDAY_START_TIME
   assert schedule.weekday_end_time == WEEKDAY_END_TIME
   assert schedule.weekend_holiday_start_time == WEEKEND_START_TIME
   assert schedule.weekend_holiday_end_time == WEEKEND_END_TIME
