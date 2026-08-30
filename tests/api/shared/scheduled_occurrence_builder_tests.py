from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date

from api_test_support.frozen_datetime import patch_database_today
import pytest

from api.models.scheduled_occurrence import ScheduledOccurrence
from api.shared.scheduled_occurrence_builder import ScheduledOccurrenceBuilder


FROZEN_TODAY = date( 2026, 6, 15 )


@dataclass
class SampleScheduleRecord():
   schedule_start_date: str
   schedule_end_date: str | None
   monday: bool
   tuesday: bool
   wednesday: bool
   thursday: bool
   friday: bool
   saturday: bool
   sunday: bool
   occurrence_time: str


@pytest.fixture
def freeze_database_today( monkeypatch: pytest.MonkeyPatch ) -> Callable[ [ date ], None ]:
   def freeze( value: date ) -> None:
      patch_database_today( monkeypatch, value )

   return freeze


def _weekday_flags( record: SampleScheduleRecord ) -> tuple[ bool, bool, bool, bool, bool, bool, bool ]:
   return (
      record.monday,
      record.tuesday,
      record.wednesday,
      record.thursday,
      record.friday,
      record.saturday,
      record.sunday,
   )


def Test_Build_TestMondaySchedule_ExpectOccurrencesForMatchingWeekdays(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )
   schedule_record = SampleScheduleRecord(
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-06-22',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      occurrence_time='10:00 AM' )

   occurrences = ScheduledOccurrenceBuilder.build(
      [ schedule_record ],
      days_ahead=7,
      get_time=lambda record: record.occurrence_time,
      get_weekday_flags=_weekday_flags,
      is_cancelled=lambda _date_key, _time: False )

   assert [ ( occurrence.date, occurrence.time ) for occurrence in occurrences ] == [
      ( '2026-06-15', '10:00 AM' ),
      ( '2026-06-22', '10:00 AM' ),
   ]


def Test_Build_TestCancelledOccurrence_ExpectExcluded(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )
   schedule_record = SampleScheduleRecord(
      schedule_start_date='2026-06-15',
      schedule_end_date='2026-06-15',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      occurrence_time='10:00 AM' )

   occurrences = ScheduledOccurrenceBuilder.build(
      [ schedule_record ],
      days_ahead=0,
      get_time=lambda record: record.occurrence_time,
      get_weekday_flags=_weekday_flags,
      is_cancelled=lambda date_key, time: date_key == '2026-06-15' and time == '10:00 AM' )

   assert occurrences == []


def Test_Build_TestExtraOccurrences_ExpectMergedSortedUnique(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )
   extra_occurrences = [
      ScheduledOccurrence( date='2026-06-16', time='11:00 AM' ),
      ScheduledOccurrence( date='2026-06-15', time='10:00 AM' ),
   ]

   occurrences = ScheduledOccurrenceBuilder.build(
      [],
      days_ahead=1,
      get_time=lambda _record: '10:00 AM',
      get_weekday_flags=lambda _record: ( True, True, True, True, True, True, True ),
      is_cancelled=lambda _date_key, _time: False,
      extra_occurrences=extra_occurrences )

   assert [ ( occurrence.date, occurrence.time ) for occurrence in occurrences ] == [
      ( '2026-06-15', '10:00 AM' ),
      ( '2026-06-16', '11:00 AM' ),
   ]
