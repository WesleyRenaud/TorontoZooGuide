from __future__ import annotations

from api.guardians.scheduling.guardians_talk_map_schedule_collapser import GuardiansTalkMapScheduleCollapser
from api.models.guardians_talk import GuardiansTalk


def Test_Collapse_TestSameTalkAndLocation_ExpectMergesTimes() -> None:
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
