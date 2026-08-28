from __future__ import annotations

from api.wild_encounters.domain.wild_encounter_name_filter import WildEncounterNameFilter


def Test_ShouldReturnEmpty_TestBlankName_ExpectTrue() -> None:
   encounter_filter = WildEncounterNameFilter( name='' )

   assert encounter_filter.should_return_empty() is True


def Test_AllowsWildEncounterName_TestNormalizedMatch_ExpectTrue() -> None:
   encounter_filter = WildEncounterNameFilter( name=' african rainforest ' )

   assert encounter_filter.allows_wild_encounter_name( 'African Rainforest' ) is True


def Test_AllowsWildEncounterName_TestDifferentName_ExpectFalse() -> None:
   encounter_filter = WildEncounterNameFilter( name='African Rainforest' )

   assert encounter_filter.allows_wild_encounter_name( 'Kangaroo' ) is False
