from __future__ import annotations

from api.guardians.scheduling.guardians_talk_map_schedule_collapser import GuardiansTalkMapScheduleCollapser
from api.models.guardians_talk import GuardiansTalk


def Test_Collapse_TestSameTalkAndLocation_ExpectMergesTimes() -> None:
   afternoon_polar_bear = GuardiansTalk(
      name='Polar Bear',
      location='Tundra Trek',
      x_coord=1.0,
      y_coord=2.0,
      start_time='2:00 PM' )
   morning_polar_bear = GuardiansTalk(
      name='Polar Bear',
      location='Tundra Trek',
      x_coord=1.0,
      y_coord=2.0,
      start_time='11:00 AM' )
   african_lion = GuardiansTalk(
      name='African Lion',
      location='Africa Savanna',
      x_coord=3.0,
      y_coord=4.0,
      start_time='10:00 AM' )
   talks = [ afternoon_polar_bear, morning_polar_bear, african_lion ]

   collapsed = GuardiansTalkMapScheduleCollapser.collapse( talks )

   polar_bear = next(
      talk for talk in collapsed if talk[ 'name' ] == morning_polar_bear.name )

   assert len( collapsed ) == 2
   assert polar_bear[ 'start_time' ] == morning_polar_bear.start_time
   assert polar_bear[ 'times' ] == [
      morning_polar_bear.start_time,
      afternoon_polar_bear.start_time,
   ]
   assert polar_bear[ 'end_time' ] is None
