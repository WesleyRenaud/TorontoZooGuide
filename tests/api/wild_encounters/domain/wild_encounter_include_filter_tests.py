from __future__ import annotations

from api.wild_encounters.domain.wild_encounter_include_filter import WildEncounterIncludeFilter


def Test_FromOptionalList_TestNone_ExpectAllEncountersAllowed() -> None:
   encounter_name = 'Giraffe Feeding'

   include_filter = WildEncounterIncludeFilter.from_optional_list( None )

   assert include_filter.provisioned_explicitly is False
   assert include_filter.allows_wild_encounter_name( encounter_name ) is True


def Test_ShouldReturnEmpty_TestExplicitEmptyList_ExpectTrue() -> None:
   include_filter = WildEncounterIncludeFilter.from_optional_list( [] )

   should_return_empty = include_filter.should_return_empty()

   assert should_return_empty is True


def Test_AllowsWildEncounterName_TestIncludedName_ExpectTrue() -> None:
   encounter_name = 'Giraffe Feeding'
   include_filter = WildEncounterIncludeFilter.from_optional_list(
      [ f' { encounter_name } ' ] )

   allowed = include_filter.allows_wild_encounter_name( encounter_name.lower() )

   assert allowed is True


def Test_AllowsWildEncounterName_TestExcludedName_ExpectFalse() -> None:
   encounter_name = 'Giraffe Feeding'
   other_name = 'Rhino Encounter'
   include_filter = WildEncounterIncludeFilter.from_optional_list( [ encounter_name ] )

   allowed = include_filter.allows_wild_encounter_name( other_name )

   assert allowed is False
