from __future__ import annotations

from api.models.wild_encounter import WildEncounter
from api.wild_encounters.scheduling.collapse_wild_encounters_for_map_builder import CollapseWildEncountersForMapBuilder


def Test_Build_TestSameEncounter_ExpectMergesTimes() -> None:
   encounters = [
      WildEncounter(
         name='Kangaroo',
         meeting_spot='Australasia',
         link='',
         start_time='3:00 PM',
         x_coord=5.0,
         y_coord=6.0 ),
      WildEncounter(
         name='Kangaroo',
         meeting_spot='Australasia',
         link='',
         start_time='11:00 AM',
         x_coord=5.0,
         y_coord=6.0 ),
   ]

   collapsed = CollapseWildEncountersForMapBuilder.build( encounters )

   assert len( collapsed ) == 1
   assert collapsed[ 0 ][ 'start_time' ] == '11:00 AM'
   assert collapsed[ 0 ][ 'times' ] == [ '11:00 AM', '3:00 PM' ]
   assert collapsed[ 0 ][ 'end_time' ] is None
