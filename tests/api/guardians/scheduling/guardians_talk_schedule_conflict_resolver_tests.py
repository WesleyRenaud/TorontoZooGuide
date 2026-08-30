from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import cast

import pytest

from api.guardians.data_access.guardians_talk_schedule_provider import GuardiansTalkScheduleProvider
from api.guardians.data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from api.guardians.scheduling.guardians_talk_schedule_conflict_resolver import GuardiansTalkScheduleConflictResolver
from api.guardians.scheduling.guardians_talk_schedule_input import GuardiansTalkScheduleInput
from api.shared.opening_schedule_conflict_saver import OpeningScheduleConflictSaver
from api.shared.opening_schedule_conflict_trimmer import OpeningScheduleConflictTrimmer
from api.types import Types


TALK_NAME = 'African Lion'
TALK_LOCATION = 'Africa Savanna'
TALK_TIME = '10:00 AM'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'June schedule.'


@dataclass
class StubConnection():
   pass


STUB_CONNECTION = cast( Types.Connection, StubConnection() )


def _schedule_input( *, talk_time: str = TALK_TIME ) -> GuardiansTalkScheduleInput:
   return GuardiansTalkScheduleInput(
      talk_name=TALK_NAME,
      location=TALK_LOCATION,
      start_date=START_DATE,
      end_date=END_DATE,
      talk_time=talk_time,
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=MESSAGE )


def _schedule_record() -> GuardiansTalkScheduleRecord:
   return GuardiansTalkScheduleRecord(
      name=TALK_NAME,
      location=TALK_LOCATION,
      x_coord=0.0,
      y_coord=0.0,
      maximum_duration=30,
      schedule_start_date=START_DATE,
      schedule_end_date=END_DATE,
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      talk_time=TALK_TIME )


def Test_SaveReplacingOverlaps_TestSchedule_ExpectProviderBackedSaver(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   schedule = _schedule_input()
   saver_calls: list[ tuple[ GuardiansTalkScheduleInput, Any ] ] = []

   def save_replacing_overlaps(
         _conn: Types.Connection,
         item: GuardiansTalkScheduleInput,
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

   assert GuardiansTalkScheduleConflictResolver.save_replacing_overlaps(
      STUB_CONNECTION,
      schedule ) is True
   assert saver_calls == [
      ( schedule, GuardiansTalkScheduleProvider.fetch_schedule_conflicts ),
   ]


def Test_SaveTrimmingOverlaps_TestSchedule_ExpectProviderBackedSaver(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   schedule = _schedule_input()
   saver_calls: list[ GuardiansTalkScheduleInput ] = []

   def save_trimming_overlaps(
         _conn: Types.Connection,
         item: GuardiansTalkScheduleInput,
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

   assert GuardiansTalkScheduleConflictResolver.save_trimming_overlaps(
      STUB_CONNECTION,
      schedule ) is True
   assert saver_calls == [ schedule ]


def Test_TrimConflict_TestConflictAndSchedule_ExpectTrimmerDelegation(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   conflict = _schedule_record()
   schedule = _schedule_input()
   trim_calls: list[ tuple[ GuardiansTalkScheduleRecord, GuardiansTalkScheduleInput ] ] = []

   def trim(
         _conn: Types.Connection,
         item: GuardiansTalkScheduleRecord,
         schedule_item: GuardiansTalkScheduleInput,
         *,
         delete_conflict: Any,
         update_dates: Any,
         insert_copy: Any,
   ) -> None:
      trim_calls.append( ( item, schedule_item ) )

   monkeypatch.setattr( OpeningScheduleConflictTrimmer, 'trim', trim )

   GuardiansTalkScheduleConflictResolver.trim_conflict(
      STUB_CONNECTION,
      conflict,
      schedule )

   assert trim_calls == [ ( conflict, schedule ) ]
