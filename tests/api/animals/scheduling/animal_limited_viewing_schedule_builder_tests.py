from __future__ import annotations

from api.animals.scheduling.animal_limited_viewing_schedule_builder import AnimalLimitedViewingScheduleBuilder
from api.app_string_provider import AppStringProvider
from api.shared.calendar_dates import DateValues


SPECIES = 'Western Lowland Gorilla'
EXHIBIT = 'African Rainforest Pavilion'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
DAILY_START_TIME = '10:00'
DAILY_END_TIME = '14:00'
CUSTOM_MESSAGE = 'Gorillas are visible only during the morning window.'


def Test_Build_TestCustomMessage_ExpectMappedSchedule() -> None:
   schedule = AnimalLimitedViewingScheduleBuilder.build(
      species=SPECIES,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      daily_start_time=DAILY_START_TIME,
      daily_end_time=DAILY_END_TIME,
      message=CUSTOM_MESSAGE )

   assert schedule.species == SPECIES
   assert schedule.exhibit == EXHIBIT
   assert schedule.start_date == START_DATE
   assert schedule.end_date == END_DATE
   assert schedule.daily_start_time == DAILY_START_TIME
   assert schedule.daily_end_time == DAILY_END_TIME
   assert schedule.message == CUSTOM_MESSAGE


def Test_Build_TestMissingMessageWithoutEndDate_ExpectOpenEndedGuestMessage() -> None:
   schedule = AnimalLimitedViewingScheduleBuilder.build(
      species=SPECIES,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=None,
      daily_start_time=DAILY_START_TIME,
      daily_end_time=DAILY_END_TIME,
      message='' )

   assert schedule.message == AppStringProvider.format(
      'guestStatus.animals.limitedViewingSchedule',
      species=SPECIES,
      dailyStartTime=DateValues.format_display_time_value( DAILY_START_TIME ),
      dailyEndTime=DateValues.format_display_time_value( DAILY_END_TIME ) )


def Test_Build_TestMissingMessageWithEndDate_ExpectFormattedGuestMessage() -> None:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=START_DATE,
      end_date=END_DATE )

   schedule = AnimalLimitedViewingScheduleBuilder.build(
      species=SPECIES,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      daily_start_time=DAILY_START_TIME,
      daily_end_time=DAILY_END_TIME,
      message='' )

   assert schedule.message == AppStringProvider.format(
      'guestStatus.animals.limitedViewingScheduleUntil',
      species=SPECIES,
      dailyStartTime=DateValues.format_display_time_value( DAILY_START_TIME ),
      dailyEndTime=DateValues.format_display_time_value( DAILY_END_TIME ),
      endDate=DateValues.format_display_date_value( date_range.end_date ) )
