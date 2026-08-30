from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api_test_support.frozen_datetime import patch_database_today
import pytest

from api.wild_encounters.scheduling.wild_encounter_schedule_end_builder import WildEncounterScheduleEndBuilder


ENCOUNTER_NAME = 'Giraffe Feeding'
ENCOUNTER_TIME = '2:00 PM'
SCHEDULE_END_DATE = '2026-08-31'
FROZEN_TODAY = date( 2026, 6, 15 )


@pytest.fixture
def freeze_database_today( monkeypatch: pytest.MonkeyPatch ) -> Callable[ [ date ], None ]:
   def freeze( value: date ) -> None:
      patch_database_today( monkeypatch, value )

   return freeze


def Test_Build_TestProvidedEndDate_ExpectMappedScheduleEndInput() -> None:
   schedule_end_input = WildEncounterScheduleEndBuilder.build(
      wild_encounter=ENCOUNTER_NAME,
      schedule_end_date=SCHEDULE_END_DATE,
      encounter_time=ENCOUNTER_TIME )

   assert schedule_end_input.wild_encounter == ENCOUNTER_NAME
   assert schedule_end_input.schedule_end_date == SCHEDULE_END_DATE
   assert schedule_end_input.encounter_time == ENCOUNTER_TIME


def Test_Build_TestMissingEndDate_ExpectTodayDefault(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )

   schedule_end_input = WildEncounterScheduleEndBuilder.build(
      wild_encounter=ENCOUNTER_NAME,
      schedule_end_date=None,
      encounter_time=ENCOUNTER_TIME )

   assert schedule_end_input.schedule_end_date == FROZEN_TODAY.isoformat()
