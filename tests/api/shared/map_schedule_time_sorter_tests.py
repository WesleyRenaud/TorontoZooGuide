from __future__ import annotations

from api.shared.map_schedule_time_sorter import MapScheduleTimeSorter


def Test_UniqueSorted_TestDuplicateAndMixedFormats_ExpectNormalizedAscendingTimes() -> None:
   times = MapScheduleTimeSorter.unique_sorted( [
      '3:30 PM',
      '15:30',
      '2:00 PM',
      '14:00',
      'not-a-time',
   ] )

   assert times == [ '2:00 PM', '3:30 PM' ]


def Test_UniqueSorted_TestEmptyInput_ExpectEmptyList() -> None:
   assert MapScheduleTimeSorter.unique_sorted( [] ) == []
