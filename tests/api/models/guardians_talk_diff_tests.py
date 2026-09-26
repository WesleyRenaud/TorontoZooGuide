from __future__ import annotations

from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.shared.value_conversion import ValueConversion


def Test_ToDict_TestBooleanFlag_ExpectFrontendShape() -> None:
   diff = GuardiansTalkDiff(
      name='Gorilla Talk',
      is_deleted=1,
      start_time='1:00 PM',
      end_time='1:20 PM',
      location='African Rainforest' )

   result = diff.to_dict()

   assert result[ 'name' ] == diff.name
   assert result[ 'is_deleted' ] is ValueConversion.as_boolean( diff.is_deleted )
   assert result[ 'start_time' ] == diff.start_time
   assert result[ 'end_time' ] == diff.end_time
   assert result[ 'location' ] == diff.location
