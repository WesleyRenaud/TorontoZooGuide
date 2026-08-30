from __future__ import annotations

from api.shared.opening_schedule_weekday_fields_builder import OpeningScheduleWeekdayFieldsBuilder


LOCATION_NAME = 'Beavertails'
START_DATE = '2026-06-01'
END_DATE = '2026-09-30'
CUSTOM_MESSAGE = 'Closed on weekdays this season.'


def Test_Build_TestWeekdayFlags_ExpectMappedFields() -> None:
   fields = OpeningScheduleWeekdayFieldsBuilder.build(
      name=LOCATION_NAME,
      start_date=START_DATE,
      end_date=END_DATE,
      monday=True,
      tuesday=False,
      wednesday=True,
      thursday=False,
      friday=True,
      saturday=False,
      sunday=True,
      holidays_only=False,
      message=CUSTOM_MESSAGE )

   assert fields.start_date == START_DATE
   assert fields.end_date == END_DATE
   assert fields.monday is True
   assert fields.tuesday is False
   assert fields.holidays_only is False
   assert fields.message == CUSTOM_MESSAGE


def Test_Build_TestMissingMessage_ExpectDefaultNotOpenMessage() -> None:
   fields = OpeningScheduleWeekdayFieldsBuilder.build(
      name=LOCATION_NAME,
      start_date=START_DATE,
      end_date=None,
      monday=False,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=True,
      message='' )

   assert fields.end_date is None
   assert LOCATION_NAME in fields.message
