from __future__ import annotations

from api.models.guardians_talk_diff import GuardiansTalkDiff

def Test_ToDict_TestBooleanFlag_ExpectFrontendShape() -> None:
   diff = GuardiansTalkDiff(
      name='Gorilla Talk',
      is_deleted=1,
      start_time='1:00 PM',
      end_time='1:20 PM',
      location='African Rainforest' )

   assert diff.to_dict() == {
      'name': 'Gorilla Talk',
      'is_deleted': True,
      'start_time': '1:00 PM',
      'end_time': '1:20 PM',
      'location': 'African Rainforest',
   }
