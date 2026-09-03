from __future__ import annotations

from typing import Any

from api_test_support.request_connection_test_support import STUB_REQUEST_CONNECTION
import pytest

from api.attractions.data_access.attraction_hours_schedule_provider import AttractionHoursScheduleProvider
from api.attractions.data_access.attraction_hours_schedule_record import AttractionHoursScheduleRecord
from api.attractions.scheduling.attraction_hours_schedule import AttractionHoursSchedule
from api.attractions.scheduling.attraction_hours_schedule_conflict_resolver import AttractionHoursScheduleConflictResolver
from api.shared.opening_schedule_conflict_saver import OpeningScheduleConflictSaver
from api.shared.opening_schedule_conflict_trimmer import OpeningScheduleConflictTrimmer
from api.types import Types

CAROUSEL = 'Conservation Carousel'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
WEEKDAY_START = '10:00 AM'
WEEKDAY_END = '4:00 PM'
WEEKEND_START = '9:00 AM'
WEEKEND_END = '5:00 PM'


def _schedule() -> AttractionHoursSchedule:
   return AttractionHoursSchedule(
      attraction=CAROUSEL,
      start_date=START_DATE,
      end_date=END_DATE,
      weekday_start_time=WEEKDAY_START,
      weekday_end_time=WEEKDAY_END,
      weekend_holiday_start_time=WEEKEND_START,
      weekend_holiday_end_time=WEEKEND_END )


def _conflict_record() -> AttractionHoursScheduleRecord:
   return AttractionHoursScheduleRecord(
      attraction=CAROUSEL,
      schedule_start_date=START_DATE,
      schedule_end_date=END_DATE,
      weekday_start_time=WEEKDAY_START,
      weekday_end_time=WEEKDAY_END,
      weekend_holiday_start_time=WEEKEND_START,
      weekend_holiday_end_time=WEEKEND_END )


def Test_SaveReplacingOverlaps_TestSchedule_ExpectProviderBackedSaver(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   schedule = _schedule()
   saver_calls: list[ tuple[ AttractionHoursSchedule, Any ] ] = []

   def save_replacing_overlaps(
         _conn: Types.Connection,
         item: AttractionHoursSchedule,
         *,
         fetch_conflicts: Any,
         delete_conflict: Any,
         insert_or_update: Any,
   ) -> bool:
      saver_calls.append( ( item, fetch_conflicts ) )
      return True

   monkeypatch.setattr(
      OpeningScheduleConflictSaver,
      'save_replacing_overlaps',
      save_replacing_overlaps )

   assert AttractionHoursScheduleConflictResolver.save_replacing_overlaps(
      STUB_REQUEST_CONNECTION,
      schedule ) is True
   assert saver_calls == [
      ( schedule, AttractionHoursScheduleProvider.fetch_hours_schedule_conflicts ),
   ]


def Test_SaveTrimmingOverlaps_TestSchedule_ExpectProviderBackedSaver(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   schedule = _schedule()
   saver_calls: list[ AttractionHoursSchedule ] = []

   def save_trimming_overlaps(
         _conn: Types.Connection,
         item: AttractionHoursSchedule,
         *,
         fetch_conflicts: Any,
         trim_conflict: Any,
         insert_or_update: Any,
   ) -> bool:
      saver_calls.append( item )
      return True

   monkeypatch.setattr(
      OpeningScheduleConflictSaver,
      'save_trimming_overlaps',
      save_trimming_overlaps )

   assert AttractionHoursScheduleConflictResolver.save_trimming_overlaps(
      STUB_REQUEST_CONNECTION,
      schedule ) is True
   assert saver_calls == [ schedule ]


def Test_TrimConflict_TestConflictAndSchedule_ExpectTrimmerDelegation(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   conflict = _conflict_record()
   schedule = _schedule()
   trim_calls: list[ tuple[ AttractionHoursScheduleRecord, AttractionHoursSchedule ] ] = []

   def trim(
         _conn: Types.Connection,
         item: AttractionHoursScheduleRecord,
         schedule_item: AttractionHoursSchedule,
         *,
         delete_conflict: Any,
         update_dates: Any,
         insert_copy: Any,
   ) -> None:
      trim_calls.append( ( item, schedule_item ) )

   monkeypatch.setattr( OpeningScheduleConflictTrimmer, 'trim', trim )

   AttractionHoursScheduleConflictResolver.trim_conflict(
      STUB_REQUEST_CONNECTION,
      conflict,
      schedule )

   assert trim_calls == [ ( conflict, schedule ) ]
