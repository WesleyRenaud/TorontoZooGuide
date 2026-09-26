from __future__ import annotations

from api.guardians.domain.guardians_talk_include_filter import GuardiansTalkIncludeFilter


def Test_FromOptionalList_TestNone_ExpectAllTalksAllowed() -> None:
   talk_name = 'African Lion'

   include_filter = GuardiansTalkIncludeFilter.from_optional_list( None )

   assert include_filter.provisioned_explicitly is False
   assert include_filter.allows_talk_name( talk_name ) is True


def Test_ShouldReturnEmpty_TestExplicitEmptyList_ExpectTrue() -> None:
   include_filter = GuardiansTalkIncludeFilter.from_optional_list( [] )

   should_return_empty = include_filter.should_return_empty()

   assert should_return_empty is True


def Test_AllowsTalkName_TestIncludedName_ExpectTrue() -> None:
   talk_name = 'African Lion'
   include_filter = GuardiansTalkIncludeFilter.from_optional_list( [ f' { talk_name } ' ] )

   allowed = include_filter.allows_talk_name( talk_name.lower() )

   assert allowed is True


def Test_AllowsTalkName_TestExcludedName_ExpectFalse() -> None:
   talk_name = 'African Lion'
   other_name = 'Masai Giraffe'
   include_filter = GuardiansTalkIncludeFilter.from_optional_list( [ talk_name ] )

   allowed = include_filter.allows_talk_name( other_name )

   assert allowed is False
