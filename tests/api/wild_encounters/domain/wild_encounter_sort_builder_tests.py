from __future__ import annotations

from api.models.wild_encounter import WildEncounter
from api.wild_encounters.domain.wild_encounter_sort_builder import WildEncounterSortBuilder


def Test_SortByNameAndStartTime_TestMixedNamesAndTimes_ExpectSortedList() -> None:
   wild_encounters = [
      WildEncounter(
         name='Zebra Encounter',
         meeting_spot='Africa',
         link='',
         start_time='2:00 PM' ),
      WildEncounter(
         name='Giraffe Feeding',
         meeting_spot='Africa',
         link='',
         start_time='2:00 PM' ),
      WildEncounter(
         name='Giraffe Feeding',
         meeting_spot='Africa',
         link='',
         start_time='10:00 AM' ),
   ]

   WildEncounterSortBuilder.sort_by_name_and_start_time( wild_encounters )

   assert [
      ( encounter.name, encounter.start_time )
      for encounter in wild_encounters
   ] == [
      ( 'Giraffe Feeding', '10:00 AM' ),
      ( 'Giraffe Feeding', '2:00 PM' ),
      ( 'Zebra Encounter', '2:00 PM' ),
   ]
