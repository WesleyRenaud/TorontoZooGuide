from __future__ import annotations

from api.models.wild_encounter import WildEncounter
from api.wild_encounters.search.wild_encounters_matching_query_builder import WildEncountersMatchingQueryBuilder


WILD_ENCOUNTER_NAME = 'African Rainforest'
OTHER_ENCOUNTER_NAME = 'Kangaroo'


def Test_Build_TestMatchingQuery_ExpectMatchingEncounterOnly() -> None:
   rainforest = WildEncounter(
      name=WILD_ENCOUNTER_NAME,
      meeting_spot='Rainforest Pavilion',
      link='https://www.torontozoo.com/wild-encounters/african-rainforest' )
   kangaroo = WildEncounter(
      name=OTHER_ENCOUNTER_NAME,
      meeting_spot='Australasia',
      link='' )
   wild_encounters = [ rainforest, kangaroo ]
   query = 'rainforest'

   matches = WildEncountersMatchingQueryBuilder.build( wild_encounters, query )

   assert [ encounter.name for encounter in matches ] == [ rainforest.name ]


def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingEncounterOnly() -> None:
   rainforest = WildEncounter(
      name=WILD_ENCOUNTER_NAME,
      meeting_spot='Rainforest Pavilion',
      link='https://www.torontozoo.com/wild-encounters/african-rainforest' )
   kangaroo = WildEncounter(
      name=OTHER_ENCOUNTER_NAME,
      meeting_spot='Australasia',
      link='' )
   wild_encounters = [ rainforest, kangaroo ]
   query = 'rainforest'

   matches = WildEncountersMatchingQueryBuilder.filter_matching_query(
      wild_encounters,
      query )

   assert [ encounter.name for encounter in matches ] == [ rainforest.name ]
