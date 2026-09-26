from __future__ import annotations

from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.value_conversion import ValueConversion


def Test_ToDict_TestBooleanFlag_ExpectFrontendShape() -> None:
   diff = WildEncounterDiff(
      name='Kangaroo',
      is_deleted=0,
      start_time='2:00 PM',
      end_time='2:30 PM',
      meeting_spot='Wild Encounter - Eurasia Meeting Spot',
      link='https://example.test/kangaroo' )

   result = diff.to_dict()

   assert result[ 'name' ] == diff.name
   assert result[ 'is_deleted' ] is ValueConversion.as_boolean( diff.is_deleted )
   assert result[ 'start_time' ] == diff.start_time
   assert result[ 'end_time' ] == diff.end_time
   assert result[ 'meeting_spot' ] == diff.meeting_spot
   assert result[ 'link' ] == diff.link
