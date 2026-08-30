from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api_test_support.frozen_datetime import patch_database_today
import pytest

from api.guardians.data_access.guardians_talk_cancellation_record import GuardiansTalkCancellationRecord
from api.guardians.data_access.guardians_talk_occurrence_record import GuardiansTalkOccurrenceRecord
from api.guardians.data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from api.guardians.scheduling.guardians_talk_occurrences_builder import GuardiansTalkOccurrencesBuilder


FROZEN_TODAY = date( 2026, 6, 15 )
TALK_TIME = '10:00 AM'
STATION_COORD = 0.0


@pytest.fixture
def freeze_database_today( monkeypatch: pytest.MonkeyPatch ) -> Callable[ [ date ], None ]:
   def freeze( value: date ) -> None:
      patch_database_today( monkeypatch, value )

   return freeze


def _schedule_record() -> GuardiansTalkScheduleRecord:
   return GuardiansTalkScheduleRecord(
      name='African Lion',
      location='Africa Savanna',
      x_coord=STATION_COORD,
      y_coord=STATION_COORD,
      maximum_duration=30,
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-06-22',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      talk_time=TALK_TIME )


def Test_Build_TestMondaySchedule_ExpectUpcomingOccurrences(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )

   occurrences = GuardiansTalkOccurrencesBuilder.build(
      schedule_records=[ _schedule_record() ],
      cancellation_records=[],
      days_ahead=7 )

   assert [ ( occurrence.date, occurrence.time ) for occurrence in occurrences ] == [
      ( '2026-06-15', TALK_TIME ),
      ( '2026-06-22', TALK_TIME ),
   ]


def Test_IsCancelled_TestMatchingCancellation_ExpectTrue() -> None:
   cancellations = [
      GuardiansTalkCancellationRecord(
         cancellation_date='2026-06-15',
         talk_time=TALK_TIME ),
   ]

   assert GuardiansTalkOccurrencesBuilder.is_cancelled(
      cancellations,
      '2026-06-15',
      TALK_TIME )


def Test_Build_TestCancelledOccurrenceAndExtraOccurrence_ExpectFilteredMerged(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )
   cancellations = [
      GuardiansTalkCancellationRecord(
         cancellation_date='2026-06-15',
         talk_time=TALK_TIME ),
   ]
   extra_occurrences = [
      GuardiansTalkOccurrenceRecord(
         occurrence_date='2026-06-16',
         talk_time='11:00 AM' ),
   ]

   occurrences = GuardiansTalkOccurrencesBuilder.build(
      schedule_records=[ _schedule_record() ],
      cancellation_records=cancellations,
      days_ahead=7,
      occurrence_records=extra_occurrences )

   assert [ ( occurrence.date, occurrence.time ) for occurrence in occurrences ] == [
      ( '2026-06-16', '11:00 AM' ),
      ( '2026-06-22', TALK_TIME ),
   ]
