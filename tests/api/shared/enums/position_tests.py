from __future__ import annotations

from api.shared.enums.position import Position


def Test_Position_TestMembers_ExpectIndexValues() -> None:
   assert Position.FIRST == 0
   assert Position.SECOND == 1
   assert Position.THIRD == 2
   assert Position.LAST == -1


def Test_Position_TestListIndexing_ExpectElements() -> None:
   items = [ 'a', 'b', 'c' ]

   assert items[ Position.FIRST ] == 'a'
   assert items[ Position.SECOND ] == 'b'
   assert items[ Position.THIRD ] == 'c'
   assert items[ Position.LAST ] == 'c'
