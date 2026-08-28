from api.guardians.scheduling.guardians_talk_map_schedule_collapser import GuardiansTalkMapScheduleCollapser
from api.models import GuardiansTalk
from api.models import WildEncounter
from api.wild_encounters.scheduling.collapse_wild_encounters_for_map_builder import CollapseWildEncountersForMapBuilder


def test_collapse_guardians_talks_for_map_merges_times_for_same_talk() -> None:
   talks = [
      GuardiansTalk(
         name='Polar Bear',
         location='Tundra Trek',
         x_coord=1.0,
         y_coord=2.0,
         start_time='2:00 PM' ),
      GuardiansTalk(
         name='Polar Bear',
         location='Tundra Trek',
         x_coord=1.0,
         y_coord=2.0,
         start_time='11:00 AM' ),
      GuardiansTalk(
         name='African Lion',
         location='Africa Savanna',
         x_coord=3.0,
         y_coord=4.0,
         start_time='10:00 AM' ),
   ]

   collapsed = GuardiansTalkMapScheduleCollapser.collapse( talks )

   assert len( collapsed ) == 2
   polar_bear = next( talk for talk in collapsed if talk[ 'name' ] == 'Polar Bear' )
   assert polar_bear[ 'start_time' ] == '11:00 AM'
   assert polar_bear[ 'times' ] == [ '11:00 AM', '2:00 PM' ]
   assert polar_bear[ 'end_time' ] is None


def test_collapse_wild_encounters_for_map_merges_times_for_same_encounter() -> None:
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
