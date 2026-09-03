from __future__ import annotations

import pytest

from api.shared.calendar_dates import DateValues
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


def Test_UniqueSorted_TestInvalidTime_ExpectSkipped() -> None:
   assert MapScheduleTimeSorter.unique_sorted( [ 'bad-time', '10:00 AM' ] ) == [ '10:00 AM' ]


def Test_UniqueSorted_TestUnparseableSeconds_ExpectSkipped(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      DateValues,
      'time_value_in_seconds',
      lambda value: None )

   assert MapScheduleTimeSorter.unique_sorted( [ '10:00 AM' ] ) == []
