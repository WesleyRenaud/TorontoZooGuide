from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import cast

import pytest

from api.shared.opening_schedule_conflict_resolution import OpeningScheduleConflictResolution
from api.shared.opening_schedule_conflict_resolver_factory import OpeningScheduleConflictResolverFactory
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


def _fetch_conflicts(
      _conn: Types.Connection,
      _schedule: SampleSchedule,
) -> list[ SampleConflict ]:
   return []


def _delete_conflict(
      _conn: Types.Connection,
      _conflict: SampleConflict,
) -> None:
   return None


def _insert_or_update(
      _conn: Types.Connection,
      _schedule: SampleSchedule,
) -> None:
   return None


def _update_dates( *_args: Any ) -> None:
   return None


def _insert_copy( *_args: Any ) -> None:
   return None


def Test_CreateOpeningScheduleConflictResolver_TestCallables_ExpectWiredResolution() -> None:
   resolution = OpeningScheduleConflictResolverFactory.create_opening_schedule_conflict_resolver(
      fetch_conflicts=_fetch_conflicts,
      delete_conflict=_delete_conflict,
      insert_or_update=_insert_or_update,
      update_dates=_update_dates,
      insert_copy=_insert_copy )

   assert isinstance( resolution, OpeningScheduleConflictResolution )
   assert resolution.fetch_conflicts is _fetch_conflicts
   assert resolution.delete_conflict is _delete_conflict
   assert resolution.insert_or_update is _insert_or_update
   assert resolution.update_dates is _update_dates
   assert resolution.insert_copy is _insert_copy


def Test_CreateOpeningScheduleConflictResolver_TestSaveReplacingOverlaps_ExpectSaverDelegation(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   schedule = SampleSchedule( start_date='2026-06-01', end_date='2026-06-30' )
   calls: list[ Any ] = []

   def save_replacing_overlaps(
         _conn: Types.Connection,
         item: SampleSchedule,
         *,
         fetch_conflicts: Any,
         delete_conflict: Any,
         insert_or_update: Any,
   ) -> bool:
      calls.append( ( item, fetch_conflicts, delete_conflict, insert_or_update ) )
      return True

   monkeypatch.setattr(
      OpeningScheduleConflictSaver,
      'save_replacing_overlaps',
      save_replacing_overlaps )

   resolution = OpeningScheduleConflictResolverFactory.create_opening_schedule_conflict_resolver(
      fetch_conflicts=_fetch_conflicts,
      delete_conflict=_delete_conflict,
      insert_or_update=_insert_or_update,
      update_dates=_update_dates,
      insert_copy=_insert_copy )

   assert resolution.save_replacing_overlaps( STUB_CONNECTION, schedule ) is True
   assert calls == [
      ( schedule, _fetch_conflicts, _delete_conflict, _insert_or_update ),
   ]


def Test_CreateOpeningScheduleConflictResolver_TestTrimConflict_ExpectTrimmerDelegation(
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
      assert delete_conflict is _delete_conflict
      assert update_dates is _update_dates
      assert insert_copy is _insert_copy

   monkeypatch.setattr( OpeningScheduleConflictTrimmer, 'trim', trim )

   resolution = OpeningScheduleConflictResolverFactory.create_opening_schedule_conflict_resolver(
      fetch_conflicts=_fetch_conflicts,
      delete_conflict=_delete_conflict,
      insert_or_update=_insert_or_update,
      update_dates=_update_dates,
      insert_copy=_insert_copy )

   resolution.trim_conflict( STUB_CONNECTION, conflict, schedule )

   assert calls == [ ( conflict, schedule ) ]
