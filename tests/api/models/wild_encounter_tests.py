from __future__ import annotations

from api.models.wild_encounter import WildEncounter
from api.shared.value_conversion import ValueConversion


ENCOUNTER_NAME = 'Encounter'
ENCOUNTER_MEETING_SPOT = 'Spot'
ENCOUNTER_LINK = 'https://example.test'
ENCOUNTER_REGION = 'Africa'


def Test_ToDict_TestWildEncounterFields_ExpectFrontendShape() -> None:
   encounter = WildEncounter(
      name=ENCOUNTER_NAME,
      meeting_spot=ENCOUNTER_MEETING_SPOT,
      link=ENCOUNTER_LINK,
      region=ENCOUNTER_REGION )

   result = encounter.to_dict()

   assert result[ 'name' ] == encounter.name
   assert result[ 'meeting_spot' ] == encounter.meeting_spot
   assert result[ 'link' ] == encounter.link
   assert result[ 'region' ] == encounter.region
   assert result[ 'is_available' ] is ValueConversion.as_boolean( encounter.is_available )
   assert result[ 'is_deleted' ] is ValueConversion.as_boolean( encounter.is_deleted )
