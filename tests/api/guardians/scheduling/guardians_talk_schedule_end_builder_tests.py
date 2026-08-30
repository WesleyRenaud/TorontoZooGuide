from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api_test_support.frozen_datetime import patch_database_today
import pytest

from api.guardians.scheduling.guardians_talk_schedule_end_builder import GuardiansTalkScheduleEndBuilder


TALK_NAME = 'African Lion'
TALK_LOCATION = 'Africa Savanna'
TALK_TIME = '10:00 AM'
SCHEDULE_END_DATE = '2026-06-30'
FROZEN_TODAY = date( 2026, 6, 15 )


@pytest.fixture
def freeze_database_today( monkeypatch: pytest.MonkeyPatch ) -> Callable[ [ date ], None ]:
   def freeze( value: date ) -> None:
      patch_database_today( monkeypatch, value )

   return freeze


def Test_Build_TestProvidedEndDate_ExpectMappedScheduleEndInput() -> None:
   schedule_end_input = GuardiansTalkScheduleEndBuilder.build(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      schedule_end_date=SCHEDULE_END_DATE,
      talk_time=TALK_TIME )

   assert schedule_end_input.talk_name == TALK_NAME
   assert schedule_end_input.location == TALK_LOCATION
   assert schedule_end_input.schedule_end_date == SCHEDULE_END_DATE
   assert schedule_end_input.talk_time == TALK_TIME


def Test_Build_TestMissingEndDate_ExpectTodayDefault(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )

   schedule_end_input = GuardiansTalkScheduleEndBuilder.build(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      schedule_end_date=None,
      talk_time=TALK_TIME )

   assert schedule_end_input.schedule_end_date == FROZEN_TODAY.isoformat()
