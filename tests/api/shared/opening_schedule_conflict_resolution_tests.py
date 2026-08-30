from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import cast

import pytest

from api.shared.opening_schedule_conflict_resolution import OpeningScheduleConflictResolution
from api.shared.opening_schedule_conflict_saver import OpeningScheduleConflictSaver
from api.shared.opening_schedule_conflict_trimmer import OpeningScheduleConflictTrimmer
from api.types import Types


@dataclass
class SampleSchedule():
   start_date: str
   end_date: str | None


@dataclass
class SampleConflict():
   schedule_start_date: str
   schedule_end_date: str | None


STUB_CONNECTION = cast( Types.Connection, None )


def Test_SaveReplacingOverlaps_TestResolution_ExpectSaverDelegation(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   schedule = SampleSchedule( start_date='2026-06-01', end_date='2026-06-30' )
   calls: list[ str ] = []

   def save_replacing_overlaps(
         _conn: Types.Connection,
         _schedule: SampleSchedule,
         *,
         fetch_conflicts: Any,
         delete_conflict: Any,
         insert_or_update: Any,
   ) -> bool:
      calls.append( 'save_replacing_overlaps' )
      return True

   monkeypatch.setattr(
      OpeningScheduleConflictSaver,
      'save_replacing_overlaps',
      save_replacing_overlaps )

   resolution = OpeningScheduleConflictResolution(
      fetch_conflicts=lambda _conn, _schedule: [],
      delete_conflict=lambda _conn, _conflict: None,
      insert_or_update=lambda _conn, _schedule: None,
      update_dates=lambda *_args: None,
      insert_copy=lambda *_args: None )

   assert resolution.save_replacing_overlaps( STUB_CONNECTION, schedule ) is True
   assert calls == [ 'save_replacing_overlaps' ]


def Test_TrimConflict_TestResolution_ExpectTrimmerDelegation(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   schedule = SampleSchedule( start_date='2026-06-10', end_date='2026-06-20' )
   conflict = SampleConflict(
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-06-30' )
   calls: list[ tuple[ SampleConflict, SampleSchedule ] ] = []

   def trim(
         _conn: Types.Connection,
         item: SampleConflict,
         schedule_item: SampleSchedule,
         *,
         delete_conflict: Any,
         update_dates: Any,
         insert_copy: Any,
   ) -> None:
      calls.append( ( item, schedule_item ) )

   monkeypatch.setattr( OpeningScheduleConflictTrimmer, 'trim', trim )

   resolution = OpeningScheduleConflictResolution(
      fetch_conflicts=lambda _conn, _schedule: [],
      delete_conflict=lambda _conn, _conflict: None,
      insert_or_update=lambda _conn, _schedule: None,
      update_dates=lambda *_args: None,
      insert_copy=lambda *_args: None )

   resolution.trim_conflict( STUB_CONNECTION, conflict, schedule )

   assert calls == [ ( conflict, schedule ) ]
