from __future__ import annotations

from api.animals.scheduling.animal_limited_viewing_schedule_builder import AnimalLimitedViewingScheduleBuilder


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


def Test_Build_TestMissingMessageWithEndDate_ExpectFormattedGuestMessage() -> None:
   schedule = AnimalLimitedViewingScheduleBuilder.build(
      species=SPECIES,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      daily_start_time=DAILY_START_TIME,
      daily_end_time=DAILY_END_TIME,
      message='' )

   assert SPECIES in schedule.message
   assert '10:00 AM' in schedule.message
   assert '2:00 PM' in schedule.message
   assert '2026' in schedule.message
