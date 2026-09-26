from __future__ import annotations

from api.guardians.domain.guardians_talk_name_filter import GuardiansTalkNameFilter


def Test_ShouldReturnEmpty_TestBlankName_ExpectTrue() -> None:
   name = '   '
   talk_filter = GuardiansTalkNameFilter( name=name )

   should_return_empty = talk_filter.should_return_empty()

   assert should_return_empty is True


def Test_AllowsTalkName_TestNormalizedMatch_ExpectTrue() -> None:
   name = 'African Lion'
   talk_filter = GuardiansTalkNameFilter( name=f' { name } ' )

   allowed = talk_filter.allows_talk_name( name.upper() )

   assert allowed is True


def Test_AllowsTalkName_TestDifferentName_ExpectFalse() -> None:
   name = 'African Lion'
   other_name = 'Polar Bear'
   talk_filter = GuardiansTalkNameFilter( name=name )

   allowed = talk_filter.allows_talk_name( other_name )

   assert allowed is False
