from __future__ import annotations

from api.wild_encounters.domain.wild_encounter_include_filter import WildEncounterIncludeFilter


def Test_FromOptionalList_TestNone_ExpectAllEncountersAllowed() -> None:
   include_filter = WildEncounterIncludeFilter.from_optional_list( None )

   assert include_filter.provisioned_explicitly is False
   assert include_filter.allows_wild_encounter_name( 'Giraffe Feeding' )


def Test_ShouldReturnEmpty_TestExplicitEmptyList_ExpectTrue() -> None:
   include_filter = WildEncounterIncludeFilter.from_optional_list( [] )

   assert include_filter.should_return_empty()


def Test_AllowsWildEncounterName_TestIncludedName_ExpectTrue() -> None:
   include_filter = WildEncounterIncludeFilter.from_optional_list( [ ' Giraffe Feeding ' ] )

   assert include_filter.allows_wild_encounter_name( 'giraffe feeding' )


def Test_AllowsWildEncounterName_TestExcludedName_ExpectFalse() -> None:
   include_filter = WildEncounterIncludeFilter.from_optional_list( [ 'Giraffe Feeding' ] )

   assert not include_filter.allows_wild_encounter_name( 'Rhino Encounter' )
