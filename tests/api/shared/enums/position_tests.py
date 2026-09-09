from __future__ import annotations

from api.shared.enums.position import Position
from api.shared.enums.shared_enum_values import SharedEnumValues


def Test_Position_TestSharedJson_ExpectSingleSourceOfTruth() -> None:
   shared_members = SharedEnumValues.load_integers( 'position.json' )
   actual = {
      name: member.value
      for name, member in Position.__members__.items()
   }

   assert actual == shared_members


def Test_Position_TestListIndexing_ExpectElements() -> None:
   items = [ 'a', 'b', 'c' ]

   assert items[ Position.FIRST ] == 'a'
   assert items[ Position.SECOND ] == 'b'
   assert items[ Position.THIRD ] == 'c'
   assert items[ Position.LAST ] == 'c'
