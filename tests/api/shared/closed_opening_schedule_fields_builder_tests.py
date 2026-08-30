from __future__ import annotations

from api.shared.closed_opening_schedule_fields_builder import ClosedOpeningScheduleFieldsBuilder


LOCATION_NAME = 'Zoomobile Station'
START_DATE = '2026-06-01'
END_DATE = '2026-06-15'
CUSTOM_MESSAGE = 'Station closed for route maintenance.'


def Test_Build_TestCustomMessage_ExpectAllWeekdaysClosed() -> None:
   fields = ClosedOpeningScheduleFieldsBuilder.build(
      name=LOCATION_NAME,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CUSTOM_MESSAGE )

   assert fields.start_date == START_DATE
   assert fields.end_date == END_DATE
   assert fields.monday is False
   assert fields.tuesday is False
   assert fields.wednesday is False
   assert fields.thursday is False
   assert fields.friday is False
   assert fields.saturday is False
   assert fields.sunday is False
   assert fields.holidays_only is False
   assert fields.message == CUSTOM_MESSAGE


def Test_Build_TestMissingMessage_ExpectDefaultClosedMessage() -> None:
   fields = ClosedOpeningScheduleFieldsBuilder.build(
      name=LOCATION_NAME,
      start_date=START_DATE,
      end_date=None,
      message='' )

   assert fields.end_date is None
   assert LOCATION_NAME in fields.message
