from __future__ import annotations

from api.guardians.domain.guardians_talk_name_filter import GuardiansTalkNameFilter


def Test_ShouldReturnEmpty_TestBlankName_ExpectTrue() -> None:
   talk_filter = GuardiansTalkNameFilter( name='   ' )

   assert talk_filter.should_return_empty() is True


def Test_AllowsTalkName_TestNormalizedMatch_ExpectTrue() -> None:
   talk_filter = GuardiansTalkNameFilter( name=' African Lion ' )

   assert talk_filter.allows_talk_name( 'AFRICAN LION' ) is True


def Test_AllowsTalkName_TestDifferentName_ExpectFalse() -> None:
   talk_filter = GuardiansTalkNameFilter( name='African Lion' )

   assert talk_filter.allows_talk_name( 'Polar Bear' ) is False
