from __future__ import annotations

from dataclasses import dataclass

from api.shared.scheduled_occurrence_sorter import ScheduledOccurrenceSorter


@dataclass
class SampleOccurrence():
   date: str
   time: str


def Test_UniqueSortedByKey_TestDuplicateKeys_ExpectKeepsLastItemPerKey() -> None:
   occurrences = [
      SampleOccurrence( date='2026-06-15', time='10:00 AM' ),
      SampleOccurrence( date='2026-06-15', time='10:00 AM' ),
      SampleOccurrence( date='2026-06-16', time='11:00 AM' ),
   ]

   sorted_occurrences = ScheduledOccurrenceSorter.unique_sorted_by_key(
      occurrences,
      key=lambda occurrence: ( occurrence.date, occurrence.time ),
      sort_key=lambda occurrence: ( occurrence.date, occurrence.time ) )

   assert [ ( item.date, item.time ) for item in sorted_occurrences ] == [
      ( '2026-06-15', '10:00 AM' ),
      ( '2026-06-16', '11:00 AM' ),
   ]
