from __future__ import annotations

from dataclasses import dataclass

from api.shared.map_schedule_occurrence_collapser import MapScheduleOccurrenceCollapser
from api.shared.map_schedule_time_sorter import MapScheduleTimeSorter


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
   later_polar_bear = SampleOccurrence(
      name='Polar Bear',
      location='Tundra Trek',
      start_time='2:00 PM' )
   earlier_polar_bear = SampleOccurrence(
      name=later_polar_bear.name,
      location=later_polar_bear.location,
      start_time='11:00 AM' )
   lion = SampleOccurrence(
      name='African Lion',
      location='Africa Savanna',
      start_time='10:00 AM' )
   occurrences = [ later_polar_bear, earlier_polar_bear, lion ]

   collapsed = MapScheduleOccurrenceCollapser.collapse(
      occurrences,
      group_key=lambda occurrence: ( occurrence.name, occurrence.location ),
      get_start_time=lambda occurrence: occurrence.start_time )

   polar_bear = next(
      item for item in collapsed if item[ 'name' ] == later_polar_bear.name )
   polar_bear_times = MapScheduleTimeSorter.unique_sorted( [
      later_polar_bear.start_time,
      earlier_polar_bear.start_time,
   ] )
   assert polar_bear[ 'start_time' ] == earlier_polar_bear.start_time
   assert polar_bear[ 'times' ] == polar_bear_times
   assert polar_bear[ 'end_time' ] is None
   assert len( collapsed ) == len( {
      ( occurrence.name, occurrence.location ) for occurrence in occurrences
   } )


def Test_Collapse_TestEmptyInput_ExpectEmptyList() -> None:
   occurrences: list[ SampleOccurrence ] = []

   collapsed = MapScheduleOccurrenceCollapser.collapse(
      occurrences,
      group_key=lambda occurrence: occurrence.name,
      get_start_time=lambda occurrence: occurrence.start_time )

   assert collapsed == []
