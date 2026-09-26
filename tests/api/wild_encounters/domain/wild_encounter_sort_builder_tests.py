from __future__ import annotations

from api.models.wild_encounter import WildEncounter
from api.wild_encounters.domain.wild_encounter_sort_builder import WildEncounterSortBuilder


def Test_SortByNameAndStartTime_TestMixedNamesAndTimes_ExpectSortedList() -> None:
   afternoon_zebra = WildEncounter(
      name='Zebra Encounter',
      meeting_spot='Africa',
      link='',
      start_time='2:00 PM' )
   afternoon_giraffe = WildEncounter(
      name='Giraffe Feeding',
      meeting_spot='Africa',
      link='',
      start_time='2:00 PM' )
   morning_giraffe = WildEncounter(
      name='Giraffe Feeding',
      meeting_spot='Africa',
      link='',
      start_time='10:00 AM' )
   wild_encounters = [ afternoon_zebra, afternoon_giraffe, morning_giraffe ]

   WildEncounterSortBuilder.sort_by_name_and_start_time( wild_encounters )

   assert [
      ( encounter.name, encounter.start_time )
      for encounter in wild_encounters
   ] == [
      ( morning_giraffe.name, morning_giraffe.start_time ),
      ( afternoon_giraffe.name, afternoon_giraffe.start_time ),
      ( afternoon_zebra.name, afternoon_zebra.start_time ),
   ]
