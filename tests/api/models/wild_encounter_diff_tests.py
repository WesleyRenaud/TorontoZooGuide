from __future__ import annotations

from api.models.wild_encounter_diff import WildEncounterDiff

def Test_ToDict_TestBooleanFlag_ExpectFrontendShape() -> None:
   diff = WildEncounterDiff(
      name='Kangaroo',
      is_deleted=0,
      start_time='2:00 PM',
      end_time='2:30 PM',
      meeting_spot='Wild Encounter - Eurasia Meeting Spot',
      link='https://example.test/kangaroo' )

   assert diff.to_dict() == {
      'name': 'Kangaroo',
      'is_deleted': False,
      'start_time': '2:00 PM',
      'end_time': '2:30 PM',
      'meeting_spot': 'Wild Encounter - Eurasia Meeting Spot',
      'link': 'https://example.test/kangaroo',
   }
