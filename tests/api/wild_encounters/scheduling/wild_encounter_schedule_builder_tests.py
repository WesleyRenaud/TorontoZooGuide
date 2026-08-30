from __future__ import annotations

from api.wild_encounters.scheduling.wild_encounter_schedule_builder import WildEncounterScheduleBuilder


ENCOUNTER_NAME = 'Giraffe Feeding'
START_DATE = '2026-06-01'
END_DATE = '2026-08-31'
ENCOUNTER_TIME = '2:00 PM'
CUSTOM_MESSAGE = 'Encounter not offered today.'


def Test_Build_TestCustomMessage_ExpectMappedScheduleInput() -> None:
   schedule_input = WildEncounterScheduleBuilder.build(
      wild_encounter=ENCOUNTER_NAME,
      start_date=START_DATE,
      end_date=END_DATE,
      encounter_time=ENCOUNTER_TIME,
      monday=False,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=True,
      saturday=True,
      sunday=True,
      message=CUSTOM_MESSAGE )

   assert schedule_input.wild_encounter == ENCOUNTER_NAME
   assert schedule_input.start_date == START_DATE
   assert schedule_input.end_date == END_DATE
   assert schedule_input.encounter_time == ENCOUNTER_TIME
   assert schedule_input.friday is True
   assert schedule_input.message == CUSTOM_MESSAGE


def Test_Build_TestMissingMessage_ExpectDefaultNotScheduledMessage() -> None:
   schedule_input = WildEncounterScheduleBuilder.build(
      wild_encounter=ENCOUNTER_NAME,
      start_date=START_DATE,
      end_date=None,
      encounter_time=ENCOUNTER_TIME,
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message='' )

   assert schedule_input.end_date is None
   assert ENCOUNTER_NAME in schedule_input.message
