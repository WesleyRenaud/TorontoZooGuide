from __future__ import annotations

from api.models.wild_encounter import WildEncounter
from api.wild_encounters.search.wild_encounters_matching_query_builder import WildEncountersMatchingQueryBuilder


WILD_ENCOUNTER_NAME = 'African Rainforest'
OTHER_ENCOUNTER_NAME = 'Kangaroo'


def Test_Build_TestMatchingQuery_ExpectMatchingEncounterOnly() -> None:
   wild_encounters = [
      WildEncounter(
         name=WILD_ENCOUNTER_NAME,
         meeting_spot='Rainforest Pavilion',
         link='https://www.torontozoo.com/wild-encounters/african-rainforest' ),
      WildEncounter(
         name=OTHER_ENCOUNTER_NAME,
         meeting_spot='Australasia',
         link='' ),
   ]

   matches = WildEncountersMatchingQueryBuilder.build( wild_encounters, 'rainforest' )

   assert [ encounter.name for encounter in matches ] == [ WILD_ENCOUNTER_NAME ]

def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingEncounterOnly() -> None:
   wild_encounters = [
      WildEncounter(
         name=WILD_ENCOUNTER_NAME,
         meeting_spot='Rainforest Pavilion',
         link='https://www.torontozoo.com/wild-encounters/african-rainforest' ),
      WildEncounter(
         name=OTHER_ENCOUNTER_NAME,
         meeting_spot='Australasia',
         link='' ),
   ]
   matches = WildEncountersMatchingQueryBuilder.filter_matching_query( wild_encounters, 'rainforest' )
   assert [ encounter.name for encounter in matches ] == [ WILD_ENCOUNTER_NAME ]
