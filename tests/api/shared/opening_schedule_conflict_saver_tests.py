from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from api.shared.opening_schedule_conflict_saver import OpeningScheduleConflictSaver
from api.types import Types


@dataclass
class SampleSchedule():
   start_date: str
   end_date: str | None


@dataclass
class StubConnection():
   commits: int = 0

   def commit( self ) -> None:
      self.commits += 1


def Test_SaveReplacingOverlaps_TestConflicts_ExpectDeleteInsertAndCommit() -> None:
   schedule = SampleSchedule( start_date='2026-06-01', end_date='2026-06-30' )
   conn = StubConnection()
   conflicts = [ object(), object() ]
   deleted: list[ object ] = []
   inserted: list[ SampleSchedule ] = []

   saved = OpeningScheduleConflictSaver.save_replacing_overlaps(
      cast( Types.Connection, conn ),
      schedule,
      fetch_conflicts=lambda _conn, _schedule: conflicts,
      delete_conflict=lambda _conn, conflict: deleted.append( conflict ),
      insert_or_update=lambda _conn, item: inserted.append( item ) )

   assert saved is True
   assert deleted == conflicts
   assert inserted == [ schedule ]
   assert conn.commits == 1


def Test_SaveTrimmingOverlaps_TestConflicts_ExpectTrimInsertAndCommit() -> None:
   schedule = SampleSchedule( start_date='2026-06-01', end_date='2026-06-30' )
   conn = StubConnection()
   conflicts = [ object() ]
   trimmed: list[ tuple[ object, SampleSchedule ] ] = []
   inserted: list[ SampleSchedule ] = []

   saved = OpeningScheduleConflictSaver.save_trimming_overlaps(
      cast( Types.Connection, conn ),
      schedule,
      fetch_conflicts=lambda _conn, _schedule: conflicts,
      trim_conflict=lambda _conn, conflict, item: trimmed.append( ( conflict, item ) ),
      insert_or_update=lambda _conn, item: inserted.append( item ) )

   assert saved is True
   assert len( trimmed ) == 1
   assert trimmed[ 0 ][ 1 ] == schedule
   assert inserted == [ schedule ]
   assert conn.commits == 1
