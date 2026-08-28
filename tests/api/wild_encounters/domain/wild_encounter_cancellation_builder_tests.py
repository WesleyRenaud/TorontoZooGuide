from __future__ import annotations

from api.wild_encounters.cancellations.wild_encounter_cancellation_builder import WildEncounterCancellationBuilder


WILD_ENCOUNTER_NAME = 'African Rainforest'
CANCELLATION_DATE = '2026-06-15'
ENCOUNTER_TIME = '2:00 PM'


def Test_Build_TestWildEncounterCancellation_ExpectMapsFields() -> None:
   cancellation = WildEncounterCancellationBuilder.build(
      wild_encounter=WILD_ENCOUNTER_NAME,
      date=CANCELLATION_DATE,
      time=ENCOUNTER_TIME )

   assert cancellation.wild_encounter == WILD_ENCOUNTER_NAME
   assert cancellation.cancellation_date == CANCELLATION_DATE
   assert cancellation.encounter_time == ENCOUNTER_TIME
