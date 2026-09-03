from __future__ import annotations

from typing import Any

from api_test_support.request_connection_test_support import STUB_REQUEST_CONNECTION
import pytest

from api.attractions.data_access.attraction_schedule_provider import AttractionScheduleProvider
from api.attractions.data_access.attraction_schedule_record import AttractionScheduleRecord
from api.attractions.scheduling.attraction_opening_schedule import AttractionOpeningSchedule
from api.attractions.scheduling.attraction_schedule_conflict_resolver import AttractionScheduleConflictResolver
from api.shared.opening_schedule_conflict_saver import OpeningScheduleConflictSaver
from api.shared.opening_schedule_conflict_trimmer import OpeningScheduleConflictTrimmer
from api.types import Types

CAROUSEL = 'Conservation Carousel'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'Seasonal hours.'


def _schedule() -> AttractionOpeningSchedule:
   return AttractionOpeningSchedule(
      attraction=CAROUSEL,
      start_date=START_DATE,
      end_date=END_DATE,
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message=MESSAGE )


def _conflict_record() -> AttractionScheduleRecord:
   return AttractionScheduleRecord(
      attraction=CAROUSEL,
      schedule_start_date=START_DATE,
      schedule_end_date=END_DATE,
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      schedule_message=MESSAGE )


def Test_SaveReplacingOverlaps_TestSchedule_ExpectProviderBackedSaver(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   schedule = _schedule()
   saver_calls: list[ tuple[ AttractionOpeningSchedule, Any ] ] = []

   def save_replacing_overlaps(
         _conn: Types.Connection,
         item: AttractionOpeningSchedule,
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

   assert AttractionScheduleConflictResolver.save_replacing_overlaps(
      STUB_REQUEST_CONNECTION,
      schedule ) is True
   assert saver_calls == [
      ( schedule, AttractionScheduleProvider.fetch_opening_schedule_conflicts ),
   ]


def Test_SaveTrimmingOverlaps_TestSchedule_ExpectProviderBackedSaver(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   schedule = _schedule()
   saver_calls: list[ AttractionOpeningSchedule ] = []

   def save_trimming_overlaps(
         _conn: Types.Connection,
         item: AttractionOpeningSchedule,
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

   assert AttractionScheduleConflictResolver.save_trimming_overlaps(
      STUB_REQUEST_CONNECTION,
      schedule ) is True
   assert saver_calls == [ schedule ]


def Test_TrimConflict_TestConflictAndSchedule_ExpectTrimmerDelegation(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   conflict = _conflict_record()
   schedule = _schedule()
   trim_calls: list[ tuple[ AttractionScheduleRecord, AttractionOpeningSchedule ] ] = []

   def trim(
         _conn: Types.Connection,
         item: AttractionScheduleRecord,
         schedule_item: AttractionOpeningSchedule,
         *,
         delete_conflict: Any,
         update_dates: Any,
         insert_copy: Any,
   ) -> None:
      trim_calls.append( ( item, schedule_item ) )

   monkeypatch.setattr( OpeningScheduleConflictTrimmer, 'trim', trim )

   AttractionScheduleConflictResolver.trim_conflict(
      STUB_REQUEST_CONNECTION,
      conflict,
      schedule )

   assert trim_calls == [ ( conflict, schedule ) ]
