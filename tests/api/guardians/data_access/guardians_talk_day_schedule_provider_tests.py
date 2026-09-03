from __future__ import annotations

from api_test_support.request_connection_test_support import STUB_REQUEST_CONNECTION
import pytest

from api.guardians.data_access.guardians_talk_day_schedule_provider import GuardiansTalkDayScheduleProvider
from api.guardians.data_access.guardians_talk_day_schedule_record import GuardiansTalkDayScheduleRecord
from api.guardians.data_access.guardians_talk_occurrence_provider import GuardiansTalkOccurrenceProvider
from api.guardians.data_access.guardians_talk_schedule_provider import GuardiansTalkScheduleProvider
from api.guardians.data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from api.types import Types

TALK_NAME = 'African Lion'
TALK_LOCATION = 'Africa Savanna'
STATION_COORD = 0.0
WEDNESDAY_VISIT_DATE = '2026-06-17'
THURSDAY_VISIT_DATE = '2026-06-18'
ADDED_OCCURRENCE_DATE = '2026-06-15'
ADDED_TALK_TIME = '11:00 AM'


def _schedule_record(
      *,
      talk_time: str,
      wednesday: bool = False,
      thursday: bool = False ) -> GuardiansTalkScheduleRecord:
   return GuardiansTalkScheduleRecord(
      name=TALK_NAME,
      location=TALK_LOCATION,
      x_coord=STATION_COORD,
      y_coord=STATION_COORD,
      maximum_duration=30,
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-06-30',
      monday=False,
      tuesday=False,
      wednesday=wednesday,
      thursday=thursday,
      friday=False,
      saturday=False,
      sunday=False,
      talk_time=talk_time )


def _added_occurrence_day_record() -> GuardiansTalkDayScheduleRecord:
   return GuardiansTalkDayScheduleRecord(
      name=TALK_NAME,
      location=TALK_LOCATION,
      x_coord=STATION_COORD,
      y_coord=STATION_COORD,
      maximum_duration=30,
      talk_time=ADDED_TALK_TIME )


def Test_FetchDayScheduleRecords_TestInvalidTargetDate_ExpectEmpty(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   def fetch_day_schedule_records_from_schedule(
         _conn: Types.Connection,
         _target_date: Types.DateKey,
   ) -> list[ GuardiansTalkScheduleRecord ]:
      raise AssertionError( 'schedule provider should not be called for invalid dates' )

   monkeypatch.setattr(
      GuardiansTalkScheduleProvider,
      'fetch_day_schedule_records_from_schedule',
      fetch_day_schedule_records_from_schedule )

   assert GuardiansTalkDayScheduleProvider.fetch_day_schedule_records(
      STUB_REQUEST_CONNECTION,
      None ) == []


def Test_FetchDayScheduleRecords_TestDifferentWeekdayTimes_ExpectMatchingTalkTimeOnly(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   def fetch_day_schedule_records_from_schedule(
         _conn: Types.Connection,
         _target_date: Types.DateKey,
   ) -> list[ GuardiansTalkScheduleRecord ]:
      return [
         _schedule_record( talk_time='1:00 PM', wednesday=True ),
         _schedule_record( talk_time='2:00 PM', thursday=True ),
      ]

   def fetch_day_schedule_records_from_occurrences(
         _conn: Types.Connection,
         _target_date: Types.DateKey,
   ) -> list[ GuardiansTalkDayScheduleRecord ]:
      return []

   monkeypatch.setattr(
      GuardiansTalkScheduleProvider,
      'fetch_day_schedule_records_from_schedule',
      fetch_day_schedule_records_from_schedule )
   monkeypatch.setattr(
      GuardiansTalkOccurrenceProvider,
      'fetch_day_schedule_records_from_occurrences',
      fetch_day_schedule_records_from_occurrences )

   wednesday_records = GuardiansTalkDayScheduleProvider.fetch_day_schedule_records(
      STUB_REQUEST_CONNECTION,
      WEDNESDAY_VISIT_DATE )
   thursday_records = GuardiansTalkDayScheduleProvider.fetch_day_schedule_records(
      STUB_REQUEST_CONNECTION,
      THURSDAY_VISIT_DATE )

   assert [ record.talk_time for record in wednesday_records ] == [ '1:00 PM' ]
   assert [ record.talk_time for record in thursday_records ] == [ '2:00 PM' ]


def Test_FetchDayScheduleRecords_TestAddedOccurrenceWithoutSchedule_ExpectAddedTalkIncluded(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   def fetch_day_schedule_records_from_schedule(
         _conn: Types.Connection,
         _target_date: Types.DateKey,
   ) -> list[ GuardiansTalkScheduleRecord ]:
      return []

   def fetch_day_schedule_records_from_occurrences(
         _conn: Types.Connection,
         target_date: Types.DateKey,
   ) -> list[ GuardiansTalkDayScheduleRecord ]:
      if target_date == ADDED_OCCURRENCE_DATE:
         return [ _added_occurrence_day_record() ]

      return []

   monkeypatch.setattr(
      GuardiansTalkScheduleProvider,
      'fetch_day_schedule_records_from_schedule',
      fetch_day_schedule_records_from_schedule )
   monkeypatch.setattr(
      GuardiansTalkOccurrenceProvider,
      'fetch_day_schedule_records_from_occurrences',
      fetch_day_schedule_records_from_occurrences )

   records = GuardiansTalkDayScheduleProvider.fetch_day_schedule_records(
      STUB_REQUEST_CONNECTION,
      ADDED_OCCURRENCE_DATE )

   assert len( records ) == 1
   assert records[ 0 ].talk_time == ADDED_TALK_TIME
