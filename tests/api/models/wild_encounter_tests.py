from __future__ import annotations

from api.models.wild_encounter import WildEncounter


ENCOUNTER_NAME = 'Encounter'
ENCOUNTER_MEETING_SPOT = 'Spot'
ENCOUNTER_LINK = 'https://example.test'
ENCOUNTER_REGION = 'Africa'


def Test_ToDict_TestWildEncounterFields_ExpectFrontendShape() -> None:
   assert WildEncounter(
      name=ENCOUNTER_NAME,
      meeting_spot=ENCOUNTER_MEETING_SPOT,
      link=ENCOUNTER_LINK,
      region=ENCOUNTER_REGION,
   ).to_dict()[ 'is_available' ] is True
   assert WildEncounter(
      name=ENCOUNTER_NAME,
      meeting_spot=ENCOUNTER_MEETING_SPOT,
      link=ENCOUNTER_LINK,
      region=ENCOUNTER_REGION,
   ).to_dict()[ 'region' ] == ENCOUNTER_REGION
   assert WildEncounter(
      name=ENCOUNTER_NAME,
      meeting_spot=ENCOUNTER_MEETING_SPOT,
      link=ENCOUNTER_LINK,
   ).to_dict()[ 'is_deleted' ] is False
