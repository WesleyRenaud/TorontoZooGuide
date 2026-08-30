from __future__ import annotations

from api.guardians.occurrences.guardians_talk_occurrence_builder import GuardiansTalkOccurrenceBuilder


TALK_NAME = 'African Lion'
TALK_LOCATION = 'Africa Savanna'
OCCURRENCE_DATE = '2026-06-15'
TALK_TIME = '10:00 AM'


def Test_Build_TestOccurrencePayload_ExpectMappedOccurrenceInput() -> None:
   occurrence_input = GuardiansTalkOccurrenceBuilder.build(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      date=OCCURRENCE_DATE,
      time=TALK_TIME )

   assert occurrence_input.talk_name == TALK_NAME
   assert occurrence_input.location == TALK_LOCATION
   assert occurrence_input.occurrence_date == OCCURRENCE_DATE
   assert occurrence_input.talk_time == TALK_TIME
