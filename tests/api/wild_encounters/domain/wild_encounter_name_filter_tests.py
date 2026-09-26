from __future__ import annotations

from api.wild_encounters.domain.wild_encounter_name_filter import WildEncounterNameFilter


def Test_ShouldReturnEmpty_TestBlankName_ExpectTrue() -> None:
   name = ''
   encounter_filter = WildEncounterNameFilter( name=name )

   should_return_empty = encounter_filter.should_return_empty()

   assert should_return_empty is True


def Test_AllowsWildEncounterName_TestNormalizedMatch_ExpectTrue() -> None:
   name = 'African Rainforest'
   encounter_filter = WildEncounterNameFilter( name=f' { name.lower() } ' )

   allowed = encounter_filter.allows_wild_encounter_name( name )

   assert allowed is True


def Test_AllowsWildEncounterName_TestDifferentName_ExpectFalse() -> None:
   name = 'African Rainforest'
   other_name = 'Kangaroo'
   encounter_filter = WildEncounterNameFilter( name=name )

   allowed = encounter_filter.allows_wild_encounter_name( other_name )

   assert allowed is False
