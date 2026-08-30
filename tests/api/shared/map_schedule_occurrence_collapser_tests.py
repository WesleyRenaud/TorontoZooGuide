from __future__ import annotations

from dataclasses import dataclass

from api.shared.map_schedule_occurrence_collapser import MapScheduleOccurrenceCollapser


@dataclass
class SampleOccurrence():
   name: str
   location: str
   start_time: str


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'location': self.location,
         'start_time': self.start_time,
      }


def Test_Collapse_TestSameGroup_ExpectMergesTimesAndClearsEndTime() -> None:
   occurrences = [
      SampleOccurrence(
         name='Polar Bear',
         location='Tundra Trek',
         start_time='2:00 PM' ),
      SampleOccurrence(
         name='Polar Bear',
         location='Tundra Trek',
         start_time='11:00 AM' ),
      SampleOccurrence(
         name='African Lion',
         location='Africa Savanna',
         start_time='10:00 AM' ),
   ]

   collapsed = MapScheduleOccurrenceCollapser.collapse(
      occurrences,
      group_key=lambda occurrence: ( occurrence.name, occurrence.location ),
      get_start_time=lambda occurrence: occurrence.start_time )

   assert len( collapsed ) == 2
   polar_bear = next( item for item in collapsed if item[ 'name' ] == 'Polar Bear' )
   assert polar_bear[ 'start_time' ] == '11:00 AM'
   assert polar_bear[ 'times' ] == [ '11:00 AM', '2:00 PM' ]
   assert polar_bear[ 'end_time' ] is None


def Test_Collapse_TestEmptyInput_ExpectEmptyList() -> None:
   assert MapScheduleOccurrenceCollapser.collapse(
      [],
      group_key=lambda occurrence: occurrence.name,
      get_start_time=lambda occurrence: occurrence.start_time ) == []
