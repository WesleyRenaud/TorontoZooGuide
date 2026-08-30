from __future__ import annotations

from api.guardians.domain.guardians_talk_include_filter import GuardiansTalkIncludeFilter


def Test_FromOptionalList_TestNone_ExpectAllTalksAllowed() -> None:
   include_filter = GuardiansTalkIncludeFilter.from_optional_list( None )

   assert include_filter.provisioned_explicitly is False
   assert include_filter.allows_talk_name( 'African Lion' )


def Test_ShouldReturnEmpty_TestExplicitEmptyList_ExpectTrue() -> None:
   include_filter = GuardiansTalkIncludeFilter.from_optional_list( [] )

   assert include_filter.should_return_empty()


def Test_AllowsTalkName_TestIncludedName_ExpectTrue() -> None:
   include_filter = GuardiansTalkIncludeFilter.from_optional_list( [ ' African Lion ' ] )

   assert include_filter.allows_talk_name( 'african lion' )


def Test_AllowsTalkName_TestExcludedName_ExpectFalse() -> None:
   include_filter = GuardiansTalkIncludeFilter.from_optional_list( [ 'African Lion' ] )

   assert not include_filter.allows_talk_name( 'Masai Giraffe' )
