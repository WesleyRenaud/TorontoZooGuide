from __future__ import annotations

import pytest

from api.shared.calendar_dates import DateValues
from api.shared.map_schedule_time_sorter import MapScheduleTimeSorter


def Test_UniqueSorted_TestDuplicateAndMixedFormats_ExpectNormalizedAscendingTimes() -> None:
   earlier = '2:00 PM'
   later = '3:30 PM'
   times = [ later, '15:30', earlier, '14:00', 'not-a-time' ]
   canonical_times = [
      DateValues.normalize_schedule_time( earlier ),
      DateValues.normalize_schedule_time( later ),
   ]

   unique_times = MapScheduleTimeSorter.unique_sorted( times )

   assert unique_times == sorted(
      canonical_times,
      key=DateValues.time_value_in_seconds )


def Test_UniqueSorted_TestEmptyInput_ExpectEmptyList() -> None:
   times: list[ str ] = []

   unique_times = MapScheduleTimeSorter.unique_sorted( times )

   assert unique_times == []


def Test_UniqueSorted_TestInvalidTime_ExpectSkipped() -> None:
   valid_time = '10:00 AM'
   times = [ 'bad-time', valid_time ]

   unique_times = MapScheduleTimeSorter.unique_sorted( times )

   assert unique_times == [ DateValues.normalize_schedule_time( valid_time ) ]


def Test_UniqueSorted_TestUnparseableSeconds_ExpectSkipped(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   times = [ '10:00 AM' ]
   monkeypatch.setattr(
      DateValues,
      'time_value_in_seconds',
      lambda value: None )

   unique_times = MapScheduleTimeSorter.unique_sorted( times )

   assert unique_times == []
