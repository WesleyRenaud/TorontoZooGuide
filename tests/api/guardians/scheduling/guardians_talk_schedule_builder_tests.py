from __future__ import annotations

from api.guardians.scheduling.guardians_talk_schedule_builder import GuardiansTalkScheduleBuilder


TALK_NAME = 'African Lion'
TALK_LOCATION = 'Africa Savanna'
START_DATE = '2026-06-01'
END_DATE = '2026-09-30'
TALK_TIME = '11:00 AM'
CUSTOM_MESSAGE = 'No talk scheduled today.'


def Test_Build_TestCustomMessage_ExpectMappedScheduleInput() -> None:
   schedule_input = GuardiansTalkScheduleBuilder.build(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      start_date=START_DATE,
      end_date=END_DATE,
      talk_time=TALK_TIME,
      monday=True,
      tuesday=False,
      wednesday=True,
      thursday=False,
      friday=True,
      saturday=False,
      sunday=False,
      message=CUSTOM_MESSAGE )

   assert schedule_input.talk_name == TALK_NAME
   assert schedule_input.location == TALK_LOCATION
   assert schedule_input.start_date == START_DATE
   assert schedule_input.end_date == END_DATE
   assert schedule_input.talk_time == TALK_TIME
   assert schedule_input.monday is True
   assert schedule_input.friday is True
   assert schedule_input.message == CUSTOM_MESSAGE


def Test_Build_TestMissingMessage_ExpectDefaultNotScheduledMessage() -> None:
   schedule_input = GuardiansTalkScheduleBuilder.build(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      start_date=START_DATE,
      end_date=None,
      talk_time=TALK_TIME,
      monday=False,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message='' )

   assert schedule_input.end_date is None
   assert TALK_NAME in schedule_input.message
   assert TALK_LOCATION in schedule_input.message
