from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from datetime import timedelta

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
   occurrence_time = '10:00 AM'
   days_ahead = 7
   next_monday = FROZEN_TODAY + timedelta( days=days_ahead )
   schedule_record = SampleScheduleRecord(
      schedule_start_date='2026-06-01',
      schedule_end_date=next_monday.isoformat(),
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      occurrence_time=occurrence_time )

   occurrences = ScheduledOccurrenceBuilder.build(
      [ schedule_record ],
      days_ahead=days_ahead,
      get_time=lambda record: record.occurrence_time,
      get_weekday_flags=_weekday_flags,
      is_cancelled=lambda _date_key, _time: False )

   assert [ ( occurrence.date, occurrence.time ) for occurrence in occurrences ] == [
      ( FROZEN_TODAY.isoformat(), schedule_record.occurrence_time ),
      ( next_monday.isoformat(), schedule_record.occurrence_time ),
   ]


def Test_Build_TestCancelledOccurrence_ExpectExcluded(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )
   occurrence_time = '10:00 AM'
   schedule_record = SampleScheduleRecord(
      schedule_start_date=FROZEN_TODAY.isoformat(),
      schedule_end_date=FROZEN_TODAY.isoformat(),
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      occurrence_time=occurrence_time )

   occurrences = ScheduledOccurrenceBuilder.build(
      [ schedule_record ],
      days_ahead=0,
      get_time=lambda record: record.occurrence_time,
      get_weekday_flags=_weekday_flags,
      is_cancelled=lambda date_key, time: (
         date_key == FROZEN_TODAY.isoformat()
         and time == schedule_record.occurrence_time ) )

   assert occurrences == []


def Test_Build_TestExtraOccurrences_ExpectMergedSortedUnique(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )
   extra_occurrences = [
      ScheduledOccurrence( date='2026-06-16', time='11:00 AM' ),
      ScheduledOccurrence( date=FROZEN_TODAY.isoformat(), time='10:00 AM' ),
   ]

   occurrences = ScheduledOccurrenceBuilder.build(
      [],
      days_ahead=1,
      get_time=lambda _record: '10:00 AM',
      get_weekday_flags=lambda _record: ( True, True, True, True, True, True, True ),
      is_cancelled=lambda _date_key, _time: False,
      extra_occurrences=extra_occurrences )

   assert [ ( occurrence.date, occurrence.time ) for occurrence in occurrences ] == [
      ( extra.date, extra.time )
      for extra in sorted(
         extra_occurrences,
         key=lambda occurrence: ( occurrence.date, occurrence.time ) )
   ]


def Test_Build_TestScheduleEndsBeforeWindow_ExpectTruncatedEndDate(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )
   record = SampleScheduleRecord(
      schedule_start_date='2026-06-10',
      schedule_end_date='2026-06-14',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      occurrence_time='10:00 AM',
   )

   occurrences = ScheduledOccurrenceBuilder.build(
      [ record ],
      days_ahead=7,
      get_time=lambda row: row.occurrence_time,
      get_weekday_flags=_weekday_flags,
      is_cancelled=lambda _date_key, _time: False )

   assert occurrences == []


def Test_Build_TestEndBeforeStart_ExpectSkipped(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )
   record = SampleScheduleRecord(
      schedule_start_date='2026-06-20',
      schedule_end_date='2026-06-10',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      occurrence_time='10:00 AM',
   )

   occurrences = ScheduledOccurrenceBuilder.build(
      [ record ],
      days_ahead=7,
      get_time=lambda row: row.occurrence_time,
      get_weekday_flags=_weekday_flags,
      is_cancelled=lambda _date_key, _time: False )

   assert occurrences == []
