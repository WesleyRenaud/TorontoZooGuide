from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api_test_support.frozen_datetime import patch_database_today
import pytest

from api.wild_encounters.data_access.wild_encounter_cancellation_record import WildEncounterCancellationRecord
from api.wild_encounters.data_access.wild_encounter_schedule_record import WildEncounterScheduleRecord
from api.wild_encounters.scheduling.wild_encounter_occurrences_builder import WildEncounterOccurrencesBuilder


FROZEN_TODAY = date( 2026, 6, 15 )
ENCOUNTER_TIME = '2:00 PM'
STATION_COORD = 0.0


@pytest.fixture
def freeze_database_today( monkeypatch: pytest.MonkeyPatch ) -> Callable[ [ date ], None ]:
   def freeze( value: date ) -> None:
      patch_database_today( monkeypatch, value )

   return freeze


def _schedule_record() -> WildEncounterScheduleRecord:
   return WildEncounterScheduleRecord(
      name='Giraffe Feeding',
      meeting_spot='Africa Savanna',
      link=None,
      maximum_duration=45,
      x_coord=STATION_COORD,
      y_coord=STATION_COORD,
      region='Africa',
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-06-22',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      encounter_time=ENCOUNTER_TIME,
      is_cancelled=False )


def _all_weekdays_schedule_record() -> WildEncounterScheduleRecord:
   return WildEncounterScheduleRecord(
      name='Giraffe Feeding',
      meeting_spot='Africa Savanna',
      link=None,
      maximum_duration=45,
      x_coord=STATION_COORD,
      y_coord=STATION_COORD,
      region='Africa',
      schedule_start_date='2026-06-15',
      schedule_end_date='2026-06-21',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      encounter_time=ENCOUNTER_TIME,
      is_cancelled=False )


def Test_Build_TestMondaySchedule_ExpectUpcomingOccurrences(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )

   occurrences = WildEncounterOccurrencesBuilder.build(
      schedule_records=[ _schedule_record() ],
      cancellation_records=[],
      days_ahead=7 )

   assert [ ( occurrence.date, occurrence.time ) for occurrence in occurrences ] == [
      ( '2026-06-15', ENCOUNTER_TIME ),
      ( '2026-06-22', ENCOUNTER_TIME ),
   ]


def Test_IsCancelled_TestMatchingCancellation_ExpectTrue() -> None:
   cancellations = [
      WildEncounterCancellationRecord(
         cancellation_date='2026-06-15',
         encounter_time=ENCOUNTER_TIME ),
   ]

   assert WildEncounterOccurrencesBuilder.is_cancelled(
      cancellations,
      '2026-06-15',
      ENCOUNTER_TIME )


def Test_Build_TestAllWeekdaysWithCancellation_ExpectCancelledDateExcluded(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )
   cancellations = [
      WildEncounterCancellationRecord(
         cancellation_date='2026-06-18',
         encounter_time=ENCOUNTER_TIME ),
   ]

   occurrences = WildEncounterOccurrencesBuilder.build(
      schedule_records=[ _all_weekdays_schedule_record() ],
      cancellation_records=cancellations,
      days_ahead=6 )

   assert { occurrence.date for occurrence in occurrences } == {
      '2026-06-15',
      '2026-06-16',
      '2026-06-17',
      '2026-06-19',
      '2026-06-20',
      '2026-06-21',
   }


def Test_Build_TestCancelledOccurrence_ExpectExcluded(
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( FROZEN_TODAY )
   cancellations = [
      WildEncounterCancellationRecord(
         cancellation_date='2026-06-15',
         encounter_time=ENCOUNTER_TIME ),
   ]

   occurrences = WildEncounterOccurrencesBuilder.build(
      schedule_records=[ _schedule_record() ],
      cancellation_records=cancellations,
      days_ahead=7 )

   assert [ ( occurrence.date, occurrence.time ) for occurrence in occurrences ] == [
      ( '2026-06-22', ENCOUNTER_TIME ),
   ]
